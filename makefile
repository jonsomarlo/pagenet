
del: $(shell find -name __pycache__)
	@rm -r $^
	@rm media/asn_img/*
	@rm media/dst_img/*
	@rm media/net_img/*
	@rm media/dat_txt/*
	@rm media/*.png
