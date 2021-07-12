# IPTV资源：https://github.com/BurningC4/Chinese-IPTV
type = data.get("type")
domain = data.get("domain")
if type == "SetTVChannelRequest" and domain == "media_player":
    deltaValue = data.get("deltaValue")
    if isinstance(deltaValue, str):
        # 中文频道
        deltaValue = deltaValue.upper()
        iptv = {
            "CCTV1": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv1/HD-8000k-1080P-cctv1",
            "CCTV2": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv2/HD-8000k-1080P-cctv2",
            "CCTV3": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv3/HD-8000k-1080P-cctv3",
            "CCTV4": "http://183.207.248.71:80/cntv/live1/cctv-4/cctv-4",
            "CCTV5": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv5/HD-8000k-1080P-cctv5",
            "CCTV6": "http://183.207.248.71:80/cntv/live1/cctv-6/cctv-6",
            "CCTV7": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv7/HD-8000k-1080P-cctv7",
            "CCTV8": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv8/HD-8000k-1080P-cctv8",
            "CCTV9": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv9/HD-8000k-1080P-cctv9",
            "CCTV10": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv10/HD-8000k-1080P-cctv10",
            "CCTV11": "http://183.207.248.71:80/cntv/live1/n-cctv-11/n-cctv-11",
            "CCTV12": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv12/HD-8000k-1080P-cctv12",
            "CCTV13": "http://183.207.248.71:80/cntv/live1/cctv-13/cctv-13",
            "CCTV14": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv14/HD-8000k-1080P-cctv14",
            "CCTV15": "http://183.207.248.71:80/cntv/live1/n-cctv-15/n-cctv-15",
            "CCTV17": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-cctv17/HD-8000k-1080P-cctv17",            
            "北京卫视": "http://183.207.248.71:80/cntv/live1/HD-2500k-1080P-beijingstv/HD-2500k-1080P-beijingstv",
            "北京纪实": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-beijingjishi/HD-8000k-1080P-beijingjishi",
            "北京新闻": "http://ivi.bupt.edu.cn/hls/btv9.m3u8",
            "北京影视": "http://ivi.bupt.edu.cn/hls/btv4.m3u8",
            "北京文艺": "http://ivi.bupt.edu.cn/hls/btv2.m3u8",
            "北京财经": "http://ivi.bupt.edu.cn/hls/btv5.m3u8",
            "北京生活": "http://ivi.bupt.edu.cn/hls/btv7.m3u8",
            "北京青年": "http://ivi.bupt.edu.cn/hls/btv8.m3u8",
            "北京科教": "http://ivi.bupt.edu.cn/hls/btv3.m3u8",
            "广东卫视": "http://183.207.248.71:80/cntv/live1/n-guangdongstv/n-guangdongstv",
            "东南卫视": "http://183.207.248.71:80/cntv/live1/n-dongnanstv/n-dongnanstv",
            "东方卫视": "http://183.207.248.71:80/cntv/live1/n-dongfangstv/n-dongfangstv",
            "南方卫视": "http://183.207.248.71:80/cntv/live1/SD-4000k-576P-nanfangstv/SD-4000k-576P-nanfangstv",
            "厦门卫视": "http://183.207.248.71:80/cntv/live1/SD-4000k-576P-xiamenstv/SD-4000k-576P-xiamenstv",
            "天津卫视": "http://183.207.248.71:80/cntv/live1/HD-2500k-1080P-tianjinstv/HD-2500k-1080P-tianjinstv",
            "安徽卫视": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-anhuistv/HD-8000k-1080P-anhuistv",
            "山东卫视": "http://183.207.248.71:80/cntv/live1/HD-2500k-1080P-shandongstv/HD-2500k-1080P-shandongstv",
            "江苏卫视": "http://183.207.248.71:80/cntv/live1/HD-2500k-1080P-jiangsustv/HD-2500k-1080P-jiangsustv",
            "江西卫视": "http://183.207.248.71:80/cntv/live1/jiangxistv/jiangxistv",
            "河北卫视": "http://183.207.248.71:80/cntv/live1/n-hebeistv/n-hebeistv",
            "浙江卫视": "http://183.207.248.71:80/cntv/live1/zhejiangstv/zhejiangstv",
            "深圳卫视": "http://183.207.248.71:80/cntv/live1/HD-2500k-1080P-shenzhenstv/HD-2500k-1080P-shenzhenstv",
            "湖北卫视": "http://183.207.248.71:80/cntv/live1/HD-2500k-1080P-hubeistv/HD-2500k-1080P-hubeistv",
            "湖南卫视": "http://183.207.248.71:80/cntv/live1/hunanstv/hunanstv",
            "重庆卫视": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-chongqingstv/HD-8000k-1080P-chongqingstv",
            "黑龙江卫视": "http://183.207.248.71:80/cntv/live1/HD-8000k-1080P-heilongjiangstv/HD-8000k-1080P-heilongjiangstv",
            "四川卫视": "http://183.207.248.71:80/cntv/live1/n-sichuanstv/n-sichuanstv",
            "云南卫视": "http://183.207.248.71:80/cntv/live1/n-yntv1/n-yntv1",
            "宁夏卫视": "http://183.207.248.71:80/cntv/live1/n-ningxiastv/n-ningxiastv",
            "兵团卫视": "http://183.207.248.71:80/cntv/live1/SD-4000k-576P-bingtuanstv/SD-4000k-576P-bingtuanstv",
            "山西卫视": "http://183.207.248.71:80/cntv/live1/n-shanxistv/n-shanxistv",
            "广西卫视": "http://183.207.248.71:80/cntv/live1/n-guangxistv/n-guangxistv",
            "卡酷少儿": "http://183.207.248.71:80/cntv/live1/n-kakukaton/n-kakukaton",
            "嘉佳卡通": "http://183.207.248.71:80/cntv/live1/SD-4000k-576P-jiajiakaton/SD-4000k-576P-jiajiakaton",
            "炫动卡通": "http://183.207.248.71:80/cntv/live1/n-xuandongkaton/n-xuandongkaton",
            "金鹰卡通": "http://183.207.248.71:80/cntv/live1/n-jinyingkaton/n-jinyingkaton",
            "优漫卡通": "http://183.207.248.71:80/cntv/live1/n-youmankaton/n-youmankaton",
            "点掌财经": "http://cclive.aniu.tv/live/anzb.m3u8",
            "凤凰电影": "",
            "家庭影院频道": ""
        }
        if deltaValue in iptv:
            hass.services.call("media_player", "play_media", {
                "media_content_type": "video",
                "media_content_id": iptv[deltaValue],
                "entity_id": "media_player.android"
            }, False)
    elif isinstance(deltaValue, int):
        # 频道号码
        apps = [
            'org.xbmc.kodi',
            'com.ktcp.video',
            'com.gitvdideo.aliapp'
        ]
        if len(apps) >= deltaValue:
            hass.services.call("media_player", "select_source", {
                "source": apps[deltaValue - 1],
                "entity_id": "media_player.tian_mao_mo_he"
            }, False)
