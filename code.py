import os
import zipfile
import cv2
import numpy as np
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt

def main():
#change the location of zip file
    zip_path = r"C:\Users\LENOVO\Downloads\archive.zip"
    extract_path = "brain_mri_dataset"

    if not os.path.exists(extract_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
            print(f"ZIP dosyasi cikartildi: {extract_path}")
    else:
        print(f"ZIP daha önce cikartilmis: {extract_path}")

    yes_folder = os.path.join(extract_path, "yes")
    image_files = [f for f in os.listdir(yes_folder) if f.endswith(".jpg") or f.endswith(".png")]

    if not image_files:
        print("yes klasöründe görüntü bulunamadi.")
        return

    image_path = os.path.join(yes_folder, image_files[0])  
    print(f"Kullanilan MRI görüntüsü: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        print("Görüntü yüklenemedi.")
        return

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def show_images(title1, img1, title2, img2, cmap1=None, cmap2='gray'):
        plt.figure(figsize=(12, 6))
        plt.subplot(121), plt.imshow(img1, cmap=cmap1), plt.title(title1)
        plt.subplot(122), plt.imshow(img2, cmap=cmap2), plt.title(title2)
        plt.axis('off')
        plt.show()

    show_images("Orijinal Görüntü", cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 
                "Gri Seviye", gray_image)

    thresh_val = threshold_otsu(gray_image)
    binary = gray_image > thresh_val

    blurred = cv2.GaussianBlur(gray_image, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 2)

    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    show_images("Otsu Eşikleme", binary, "Adaptive Threshold", thresh)
    show_images("Morfolojik Acilim", opening, "Arka Plan", sure_bg)

    mask = opening.astype(np.uint8)

    color_mask = np.zeros_like(image)
    color_mask[mask == 255] = [255, 0, 0]  

    alpha = 0.5
    overlay = cv2.addWeighted(image, 1.0, color_mask, alpha, 0)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(overlay, contours, -1, (0, 255, 0), 2)  

    plt.figure(figsize=(10, 6))
    plt.imshow(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    plt.title("Tümör Maskesi Bindirilmiş Görüntü")
    plt.axis('off')
    plt.show()

    tumor_pixels = np.count_nonzero(mask)
    total_pixels = gray_image.size
    tumor_percent = (tumor_pixels / total_pixels) * 100

    print("\nSONUÇLAR:")
    print(f"Tümör Alani Piksel Sayisi: {tumor_pixels}")
    print(f"Toplam Piksel Sayisi: {total_pixels}")
    print(f"Tümör Orani: %{tumor_percent:.2f}")

    output_dir = "output_results"
    os.makedirs(output_dir, exist_ok=True)

    cv2.imwrite(os.path.join(output_dir, 'gray_image.png'), gray_image)
    cv2.imwrite(os.path.join(output_dir, 'segmentation_mask.png'), mask)
    cv2.imwrite(os.path.join(output_dir, 'overlay_result.png'), overlay)

    with open(os.path.join(output_dir, 'results.txt'), 'w') as f:
        f.write(f"Tümör Alani Piksel Sayisi: {tumor_pixels}\n")
        f.write(f"Toplam Piksel Sayisi: {total_pixels}\n")
        f.write(f"Tümörün Görüntüde Kapladiği Alan: %{tumor_percent:.2f}\n")

    print("\nTüm sonuçlar 'output_results' klasörüne kaydedildi.")

if __name__ == "__main__":
    main()
