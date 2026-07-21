const app = getApp()

Page({
  data: {
    selectedId: "",
    animId: "",
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
      return
    }
    this.setData({ selectedId: id, animId: id, from, to, fileName: "", filePath: "" })
    setTimeout(() => { this.setData({ animId: "" }) }, 400)
  },

  chooseFile() {
    const imgTypes = ["jpg", "jpeg", "png", "bmp", "gif", "webp"]
    wx.chooseMessageFile({
      count: 1,
      type: imgTypes.includes(this.data.from) ? "image" : "file",
      success: (res) => {
        const f = res.tempFiles[0]
        this.setData({ fileName: f.name, fileSizeText: this._fmt(f.size), filePath: f.path })
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
      url: `${app.globalData.apiBase}/convert?target=${to}`,
      filePath, name: "file",
      success: (res) => {
        wx.showToast({ title: res.statusCode === 200 ? "Done" : "Failed", icon: res.statusCode === 200 ? "success" : "error" })
        this.setData({ converting: false })
      },
      fail: () => {
        wx.showToast({ title: "Network error", icon: "error" })
        this.setData({ converting: false })
      }
    })
  },

  _fmt(n) {
    if (n < 1024) return n + " B"
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB"
    return (n / (1024 * 1024)).toFixed(1) + " MB"
  }
})
