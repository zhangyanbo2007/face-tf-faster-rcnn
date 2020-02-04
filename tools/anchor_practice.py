import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

size_X = 16
size_Y = 16
rpn_stride = 8  # 原图的大小就是image_size = 16*16

scales = [1, 2, 4]
ratios = [0.5, 1, 2]


def anchor_gen(size_X, size_Y, rpn_stride, scales, ratios):
    scales, ratios = np.meshgrid(scales, ratios)
    scales, ratios = scales.flatten(), ratios.flatten()
    scalesY = scales * np.sqrt(ratios)
    scalesX = scales / np.sqrt(ratios)
    shiftX = np.arange(0, size_X) * rpn_stride
    shiftY = np.arange(0, size_Y) * rpn_stride
    shiftX, shiftY = np.meshgrid(shiftX, shiftY)
    centerX, anchorX = np.meshgrid(shiftX, scalesX)
    centerY, anchorY = np.meshgrid(shiftY, scalesY)
    anchor_center = np.stack([centerY, centerX], axis=2).reshape(-1, 2)
    anchor_size = np.stack([anchorY, anchorX], axis=2).reshape(-1, 2)
    boxes = np.concatenate([anchor_center - 0.5*anchor_size, anchor_center + 0.5*anchor_size], axis=1)
    # boxes = np.concatenate((anchor_center - 0.5 * anchor_size, anchor_center + 0.5 * anchor_size), axis=1)
    return boxes


anchors = anchor_gen(size_X, size_Y, rpn_stride, scales, ratios)
anchors.shape

plt.figure(figsize=(10, 10))
img = np.ones((128, 128, 3))

plt.imshow(img)
Axs = plt.gca()

for i in range(anchors.shape[0]):
    box = anchors[i]
    rec = patches.Rectangle((box[0], box[1]), box[2]-box[0], box[3] - box[1], edgecolor="r", facecolor="none")
    Axs.add_patch(rec)
plt.show()

