const app = getApp()

Page({
  data: {
    selectedId: "",
    from: "",
    to: "",
    fileName: "",
    fileSizeText: "",
    filePath: "",
    converting: false
  },

  selectPair(e) {
    const { id, from, to } = e.currentTarget.dataset
    if (this.data.selectedId === id) {
      this.setData({ selectedId: "", from: "", to: "", fileName: "", filePath: "" })
    } else {
      this.setData({ selectedId: id, from, to, fileName: "", filePath: "" })
    }
  },

  chooseFile() {
    const { from } = this.data
    const isImage = ["jpg", "jpeg", "png", "bmp", "gif", "webp"].includes(from)
    wx.chooseMessageFile({
      count: 1,
      type: isImage ? "image" : "file",
      success: (res) => {
        const f = res.tempFiles[0]
        this.setData({
          fileName: f.name,
          fileSizeText: this._formatSize(f.size),
          filePath: f.path
        })
      }
    })
  },

  clearFile() {
    this.setData({ fileName: "", fileSizeText: "", filePath: "" })
  },

  doConvert() {
    const { filePath, to } = this.data
    this.setData({ converting: true })

    wx.uploadFile({
      url: app.globalData.apiBase + "/convert?target=" + to,
      filePath,
      name: "file",
      success: (res) => {
        wx.showToast({
          title: res.statusCode === 200 ? "Done" : "Failed",
          icon: res.statusCode === 200 ? "success" : "error"
        })
        this.setData({ converting: false })
      },
      fail: () => {
        wx.showToast({ title: "Network error", icon: "error" })
        this.setData({ converting: false })
      }
    })
  },

  _formatSize(bytes) {
    if (bytes < 1024) return bytes + " B"
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB"
    return (bytes / (1024 * 1024)).toFixed(1) + " MB"
  }
})
