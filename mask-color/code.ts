figma.showUI(__html__, { width: 300, height: 200 });

function hexToRgb(hex: string): RGB {
  const r = parseInt(hex.slice(1, 3), 16) / 255;
  const g = parseInt(hex.slice(3, 5), 16) / 255;
  const b = parseInt(hex.slice(5, 7), 16) / 255;
  return { r, g, b };
}

figma.ui.onmessage = (msg: { type: string; hex: string }) => {
  if (msg.type !== 'apply-mask') return;

  const selection = figma.currentPage.selection;

  if (selection.length !== 1) {
    figma.notify('Select exactly one node.');
    return;
  }

  const node = selection[0];

  if (!('width' in node) || !('height' in node)) {
    figma.notify('Selected node has no dimensions.');
    return;
  }

  const { width, height } = node;
  const absoluteX = node.x;
  const absoluteY = node.y;
  const parent = node.parent ?? figma.currentPage;

  // Create color rectangle
  const rect = figma.createRectangle();
  rect.resize(width, height);
  rect.x = absoluteX;
  rect.y = absoluteY;
  rect.fills = [{ type: 'SOLID', color: hexToRgb(msg.hex) }];

  // Set the input image as the mask
  (node as SceneNode & { isMask: boolean }).isMask = true;

  // Add rect to the same parent as the image
  if (parent.type !== 'PAGE' && parent.type !== 'DOCUMENT') {
    (parent as FrameNode).appendChild(rect);
  }

  // Group: image (mask) first (bottom), then color rect on top
  const groupParent = parent.type === 'DOCUMENT' ? figma.currentPage : parent;
  const group = figma.group(
    [node, rect],
    groupParent as BaseNode & ChildrenMixin
  );
  group.name = 'Masked Image';

  // Select the new group
  figma.currentPage.selection = [group];
  figma.viewport.scrollAndZoomIntoView([group]);

  figma.closePlugin('Mask applied!');
};
