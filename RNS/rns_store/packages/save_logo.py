def save(img):
    import os
    import cv2
    path_db = "logo"
    
    try:
        os.makedirs(path_db)
    except BaseException:
        pass
    path, dirs, files = next(os.walk(path_db))
    file_count = len(files)
    img_path = path_db + "/" + str(file_count + 1)  + ".jpg"
    cv2.imwrite(img_path, img)
    return img_path
