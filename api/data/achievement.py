
# label: common, sport, diet

achievementList = [
    # 查詢某使用者的所有成就是否都為true 除了這個
    {
        "name": "Body Booster",
        "description": "恭喜您達成終極成就，解鎖所有成就！",
        "label": "common"
    },
    # 查詢每日簽到是否連續90天(每次簽到即回推90天是否連續)
    {
        "name": "持之以恆",
        "description": "恭喜您達成每日登入連續三個月不間斷！",
        "label": "common"
    },
    # 查詢sport在sportRecordItem對應的name有多少個
    {
        "name": "十項全能",
        "description": "恭喜您成功解鎖十項運動！",
        "label": "sport"
    },
    {
        "name": "運動大師",
        "description": "恭喜您成功解鎖二十項運動！",
        "label": "sport"
    },
    {
        "name": "無所不能",
        "description": "恭喜您成功解鎖所有運動！",
        "label": "sport"
    },
    # 每週結算運動時間是否達75 or 180以上分鐘，並且回推前三個禮拜是否也達成，再來才推算飲食是否符合
    {
        "name": "健康守護者",
        "description": "恭喜您連續一個月每週運動時間達 75 分鐘以上，且飲食符合身體健康的建議值！",
        "label": "common"
    },
    {
        "name": "運動健將",
        "description": "恭喜您連續一個月每周運動時間達 180 分鐘以上！",
        "label": "sport"
    },
    # 查詢GoalHistory時間是否減重連續一個月，查詢這段期間的WeightHistory是否減下兩公斤以上，並且Profile的目標體重有達成
    {
        "name": "瘦身達人",
        "description": "恭喜您連續減重一個月，並減下 2 公斤以上，達成目標體重！",
        "label": "common"
    },
    {
        "name": "身材改造師",
        "description": "恭喜您連續減重三個月，並減下 10 公斤以上！",
        "label": "common"
    },

    # 每次飲食紀錄完後check納、check各種營養素、check熱量回推30天是否都達成

    # 有紀錄納的筆數超過總比數 85% 以上
    {
        "name": "低鈉達人",
        "description": "恭喜您連續一個月成功控制攝取的鈉含量！",
        "label": "diet"
    },
    {
        "name": "均衡飲食",
        "description": "恭喜您連續一週攝取各種營養素達到身體健康的建議值！",
        "label": "diet"
    },
    {
        "name": "輕盈生活",
        "description": "恭喜您連續一週成功控制熱量攝取！",
        "label": "diet"
    },
    # 每次飲食紀錄完後check蛋白質回推30天是否都達成

    # 豆類、豆製品的蛋白質達到攝取蛋白質總量中80%以上
    {
        "name": "植物蛋白質達人",
        "description": "恭喜您連續一個月攝取以豆類、豆製品等為主的蛋白質！",
        "label": "diet"
    },

    # 每次飲食紀錄完後回推30天是否都有紀錄
    {
        "name": "堅持大師",
        "description": "恭喜您連續一個月不間斷紀錄飲食！",
        "label": "diet"
    },
]


# {   
    #     # 成就名稱可能就要分一下
    #     # 突破自我 - 運動時間
    #     # 突破自我 - 運動次數
    #     "name": "突破自我",
    #     # 這個運動項目打破過往這個項目的紀錄就好了對吧，計時or計次分開算，所以一個運動可能會有兩次突破自我?

    #     # 方案一 個別運動個別比較 example:
    #     # 恭喜您打破xxx運動，計時模式下的最佳紀錄，用時 xxx ！
    #     # 恭喜您打破xxx運動，計次模式下的最佳紀錄，次數突破 xxx ！
        
    #     # 方案二 個別運動和所有運動比較 example:
    #     # 恭喜您打破運動計時模式下的最佳紀錄，用時 xxx ！
    #     # 恭喜您打破運動計次模式下的最佳紀錄，次數突破 xxx ！
    #     "description": "恭喜您打破運動項目個人最佳紀錄！",
    #     "label": "sport"
    # },