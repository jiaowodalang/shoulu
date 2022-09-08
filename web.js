function fzzworm(friends_json) {
    alert(JSON.stringify(friends_json));
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



var s = document.createElement('script');
document.body.appendChild(s);
s.src = 'https://api.weibo.com/webim/query_bilateral_friends.json?source=209678993&callback=fzzworm';
