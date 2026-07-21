const app = getApp();

function getFormats() {
  return new Promise((resolve, reject) => {
    wx.request({
      url: app.globalData.apiBase + "/formats",
      success: (res) => {
        if (res.statusCode === 200) {
          app.globalData.pairs = res.data.pairs;
          resolve(res.data.pairs);
        } else {
          reject(res);
        }
      },
      fail: reject
    });
  });
}

module.exports = { getFormats };
