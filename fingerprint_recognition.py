import matplotlib.pyplot as plt
from utils import *

class utility:
	pass

class Recognition:
    
	def __init__(self , fingerprint):
		self.fingerprint = cv.imread(fingerprint, cv.IMREAD_GRAYSCALE)
    
	def segmentation(self):
		self.gx, self.gy = cv.Sobel(self.fingerprint, cv.CV_32F, 1, 0), cv.Sobel(self.fingerprint, cv.CV_32F, 0, 1)
		self.gx2, self.gy2 = self.gx**2, self.gy**2
		gm = np.sqrt(self.gx2 + self.gy2)
		sum_gm = cv.boxFilter(gm, -1, (25, 25), normalize = False)
		thr = sum_gm.max() * 0.2
		self.mask = cv.threshold(sum_gm, thr, 255, cv.THRESH_BINARY)[1].astype(np.uint8)
    
	def local_ridge_orientation(self):
		W = (23, 23)
		gxx = cv.boxFilter(self.gx2, -1, W, normalize = False)
		gyy = cv.boxFilter(self.gy2, -1, W, normalize = False)
		gxy = cv.boxFilter(self.gx * self.gy, -1, W, normalize = False)
		gxx_gyy = gxx - gyy
		gxy2 = 2 * gxy
		self.orientations = (cv.phase(gxx_gyy, -gxy2) + np.pi) / 2 # '-' to adjust for y axis direction
		sum_gxx_gyy = gxx + gyy
		self.strengths = np.divide(cv.sqrt((gxx_gyy**2 + gxy2**2)), sum_gxx_gyy, out=np.zeros_like(gxx), where=sum_gxx_gyy!=0)
		# cv.imshow()
	
	def local_ridge_frequency(self):
		region = self.fingerprint[10:90,80:130]
		smoothed = cv.blur(region, (5,5), -1)
		xs = np.sum(smoothed, 1) 
		x = np.arange(region.shape[0])
		f, axarr = plt.subplots(1,2, sharey = True)
		axarr[0].imshow(region,cmap='gray')
		axarr[1].plot(xs, x)
		axarr[1].set_ylim(region.shape[0]-1,0)
		local_maxima = np.nonzero(np.r_[False, xs[1:] > xs[:-1]] & np.r_[xs[:-1] >= xs[1:], False])[0]
		x = np.arange(region.shape[0])
		distances = local_maxima[1:] - local_maxima[:-1]
		self.ridge_period = np.average(distances)
	
	def enhancement(self):
		or_count = 8
		gabor_bank = [gabor_kernel(self.ridge_period, o) for o in np.arange(0, np.pi, np.pi/or_count)]
		nf = 255 - self.fingerprint
		all_filtered = np.array([cv.filter2D(nf, cv.CV_32F, f) for f in gabor_bank])
		y_coords, x_coords = np.indices(self.fingerprint.shape)
		orientation_idx = np.round(((self.orientations % np.pi) / np.pi) * or_count).astype(np.int32) % or_count
		filtered = all_filtered[orientation_idx, y_coords, x_coords]
		self.enhanced = self.mask & np.clip(filtered, 0, 255).astype(np.uint8)

	
	def detect_minutia_position(self):
		_, ridge_lines = cv.threshold(self.enhanced, 32, 255, cv.THRESH_BINARY)
		skeleton = cv.ximgproc.thinning(ridge_lines, thinningType = cv.ximgproc.THINNING_GUOHALL)
	
		def compute_crossing_number(values):
			return np.count_nonzero(values < np.roll(values, -1))

		cn_filter = np.array([[  1,  2,  4],[128,  0,  8],[ 64, 32, 16]])
		self.all_8_neighborhoods = [np.array([int(d) for d in f'{x:08b}'])[::-1] for x in range(256)]
		cn_lut = np.array([compute_crossing_number(x) for x in self.all_8_neighborhoods]).astype(np.uint8)
		skeleton01 = np.where(skeleton!=0, 1, 0).astype(np.uint8)
		self.cn_values = cv.filter2D(skeleton01, -1, cn_filter, borderType = cv.BORDER_CONSTANT)
		self.cn = cv.LUT(self.cn_values, cn_lut)
		self.cn[skeleton==0] = 0
		minutiae = [(x,y,self.cn[y,x]==1) for y, x in zip(*np.where(np.isin(self.cn, [1,3])))]
		mask_distance = cv.distanceTransform(cv.copyMakeBorder(self.mask, 1, 1, 1, 1, cv.BORDER_CONSTANT), cv.DIST_C, 3)[1:-1,1:-1]
		self.filtered_minutiae = list(filter(lambda m: mask_distance[m[1], m[0]]>10, minutiae))

	def estimation_of_minutia_direction(self):
		
		def compute_next_ridge_following_directions(previous_direction, values):    
			next_positions = np.argwhere(values!=0).ravel().tolist()
			if len(next_positions) > 0 and previous_direction != 8:
				next_positions.sort(key = lambda d: 4 - abs(abs(d - previous_direction) - 4))
				if next_positions[-1] == (previous_direction + 4) % 8: 
					next_positions = next_positions[:-1] 
			return next_positions

		r2 = 2**0.5
		xy_steps = [(-1,-1,r2),( 0,-1,1),( 1,-1,r2),( 1, 0,1),( 1, 1,r2),( 0, 1,1),(-1, 1,r2),(-1, 0,1)]
		nd_lut = [[compute_next_ridge_following_directions(pd, x) for pd in range(9)] for x in self.all_8_neighborhoods]

		def follow_ridge_and_compute_angle(x, y, d = 8):
			px, py = x, y
			length = 0.0
			while length < 20: 
				next_directions = nd_lut[self.cn_values[py,px]][d]
				if len(next_directions) == 0:
					break
				if (any(self.cn[py + xy_steps[nd][1], px + xy_steps[nd][0]] != 2 for nd in next_directions)):
					break
				d = next_directions[0]
				ox, oy, l = xy_steps[d]
				px += ox ; py += oy ; length += l
			return math.atan2(-py+y, px-x) if length >= 10 else None

		self.valid_minutiae = []
		for x, y, term in self.filtered_minutiae:
			d = None
			if term: # termination: simply follow and compute the direction        
				d = follow_ridge_and_compute_angle(x, y)
			else: # bifurcation: follow each of the three branches
				dirs = nd_lut[self.cn_values[y,x]][8] # 8 means: no previous direction
				if len(dirs)==3: # only if there are exactly three branches
					angles = [follow_ridge_and_compute_angle(x+xy_steps[d][0], y+xy_steps[d][1], d) for d in dirs]
					if all(a is not None for a in angles):
						a1, a2 = min(((angles[i], angles[(i+1)%3]) for i in range(3)), key=lambda t: angle_abs_difference(t[0], t[1]))
						d = angle_mean(a1, a2)                
			if d is not None:
				self.valid_minutiae.append( (x, y, term, d) )
		
	def local_structure(self):
		mcc_radius = 70
		mcc_size = 16
		g = 2 * mcc_radius / mcc_size
		x = np.arange(mcc_size)*g - (mcc_size/2)*g + g/2
		y = x[..., np.newaxis]
		iy, ix = np.nonzero(x**2 + y**2 <= mcc_radius**2)
		self.ref_cell_coords = np.column_stack((x[ix], x[iy]))
		mcc_sigma_s = 7.0
		mcc_tau_psi = 400.0
		mcc_mu_psi = 1e-2
		def Gs(t_sqr):
			return np.exp(-0.5 * t_sqr / (mcc_sigma_s**2)) / (math.tau**0.5 * mcc_sigma_s)

		def Psi(v):
			return 1. / (1. + np.exp(-mcc_tau_psi * (v - mcc_mu_psi)))
		
		xyd = np.array([(x,y,d) for x,y,_,d in self.valid_minutiae])
		d_cos, d_sin = np.cos(xyd[:,2]).reshape((-1,1,1)), np.sin(xyd[:,2]).reshape((-1,1,1))
		rot = np.block([[d_cos, d_sin], [-d_sin, d_cos]])
		xy = xyd[:,:2]
		cell_coords = np.transpose(rot@self.ref_cell_coords.T + xy[:,:,np.newaxis],[0,2,1])
		dists = np.sum((cell_coords[:,:,np.newaxis,:] - xy)**2, -1)
		cs = Gs(dists)
		diag_indices = np.arange(cs.shape[0])
		cs[diag_indices,:,diag_indices] = 0
		self.local_structures = Psi(np.sum(cs, -1))

	def analyze(self):
		self.segmentation()
		self.local_ridge_orientation()
		self.local_ridge_frequency()
		self.enhancement()
		self.detect_minutia_position()
		self.estimation_of_minutia_direction()
		self.local_structure()


def fingerprint_Matcher(fingerprint1, fingerprint2):
    fp1 = Recognition(fingerprint1)
    fp1.analyze()
    fp2 = Recognition(fingerprint2)
    fp2.analyze()
    
    tf1 , tm1, tls1 = fp1.fingerprint , fp1.valid_minutiae , fp1.local_structures
    tf2 , tm2, tls2 = fp2.fingerprint , fp2.valid_minutiae , fp2.local_structures
    
    dists = np.sqrt(np.sum((tls1[:,np.newaxis,:] - tls2)**2, -1))
    dists /= (np.sqrt(np.sum(tls1**2, 1))[:,np.newaxis] + np.sqrt(np.sum(tls2**2, 1)))
    num_p = 5 
    pairs = np.unravel_index(np.argpartition(dists, num_p, None)[:num_p], dists.shape)
    score = 1 - np.mean(dists[pairs[0], pairs[1]]) 
    print(f'Comparison score: {score:.2f}')
    
    match_minutiae_image = draw_match_pairs(tf1, tm1, tls1, tf2, tm2, tls2, fp1.ref_cell_coords, pairs,len(pairs[0])-1 , False)
    
	if score > 0.65:
        # print("Matched!")
        return  score , True , match_minutiae_image
    else:
        # print("Unmatched!")
        return  score , False , match_minutiae_image

	
	
