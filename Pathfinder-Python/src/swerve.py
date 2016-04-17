def pf_modify_swerve_default(original, length, front_left, front_right, back_left, back_right, wheelbase_width, wheelbase_depth):
    for i in range(length):
        seg = original[i]
        fl = seg.deepcopy()
        fr = seg.deepcopy()
        bl = seg.deepcopy()
        br = seg.deepcopy()

        fl.x = seg.x - wheelbase_width / 2
        fl.y = seg.y + wheelbase_depth / 2
        fr.x = seg.x + wheelbase_width / 2
        fr.y = seg.y + wheelbase_depth / 2

        bl.x = seg.x - wheelbase_width / 2
        bl.y = seg.y - wheelbase_depth / 2
        br.x = seg.x + wheelbase_width / 2
        br.y = seg.y - wheelbase_depth / 2

        front_left[i] = fl
        front_right[i] = fr
        back_left[i] = bl
        back_right[i] = br
