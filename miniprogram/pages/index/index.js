const app = getApp();

Page({
  data: {
    sources: ["docx", "pdf", "xlsx", "jpg", "png"],
    srcIndex: 0,
    targetList: [],
    tgtIndex: 0,
    fileName: "",
    fileSizeText: "",
    filePath: "",
    converting: false,
    statusText: "选择格式并上传文件"
  },

  onLoad() {
    this.updateTargets(0);
  },

  updateTargets(srcIdx) {
    const src = this.data.sources[srcIdx];
    const allPairs = app.globalData.pairs || [];
    const targets = allPairs
      .filter(p => p.from === src)
      .map(p => p.to);
    this.setData({ targetList: targets.length ? targets : ["pdf"], tgtIndex: 0 });
  },

  onSrcChange(e) {
    const idx = parseInt(e.detail.value);
    this.setData({ srcIndex: idx });
    this.updateTargets(idx);
  },

  onTgtChange(e) {
    this.setData({ tgtIndex: parseInt(e.detail.value) });
  },

  chooseFile() {
    const src = this.data.sources[this.data.srcIndex];
    const exts = ["jpg", "jpeg", "png", "bmp", "gif", "webp"].includes(src) ? ["jpg", "jpeg", "png", "bmp", "gif", "webp"] : [src];
    // Normalize extensions for wx.chooseMessageFile
    const count = exts.length;
    // WeChat Mini Program API: chooseMessageFile requires type 'all', 'image', 'video', 'file'
    const fileType = ["jpg", "jpeg", "png", "bmp", "gif", "webp"].includes(src) ? "image" : "file";
    wx.chooseMessageFile({
      count: 1,
      type: fileType,
      success: (res) => {
        const file = res.tempFiles[0];
        this.setData({
          fileName: file.name,
          fileSizeText: this.formatSize(file.size),
          filePath: file.path
        });
      }
    });
  },

  formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(1) + " MB";
  },

  doConvert() {
    const { filePath, srcIndex, tgtIndex, targetList, sources } = this.data;
    const target = targetList[tgtIndex];
    const source = sources[srcIndex];

    this.setData({ converting: true, statusText: "转换中..." });

    wx.uploadFile({
      url: app.globalData.apiBase + "/convert?target=" + target,
      filePath: filePath,
      name: "file",
      success: (res) => {
        if (res.statusCode === 200) {
          // On success, open the converted file
          const tmpPath = res.tempFilePath;
          wx.showToast({ title: "转换完成", icon: "success" });
          // For WeChat, we'd save to album or share
        } else {
          wx.showToast({ title: "转换失败", icon: "error" });
        }
        this.setData({ converting: false, statusText: "选择格式并上传文件" });
      },
      fail: () => {
        wx.showToast({ title: "网络错误", icon: "error" });
        this.setData({ converting: false, statusText: "选择格式并上传文件" });
      }
    });
  }
});
