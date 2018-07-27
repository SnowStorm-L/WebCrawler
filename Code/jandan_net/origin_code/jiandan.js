function jandan_load_img(b) {
    var d = $(b);
    var f = d.next("span.img-hash");
    var e = f.text();
    f.remove();
    var c = jdzE1jKCsUewouUTToLQXyTGTvGm6kJ8Bj(e, "cPUY9gzQmFTubb1z4qdRFw7PQaN63Kgg");
    var a = $('<a href="' + c.replace(/(\/\/\w+\.sinaimg\.cn\/)(\w+)(\/.+\.(gif|jpg|jpeg))/, "$1large$3") + '" target="_blank" class="view_img_link">[æŸ¥çœ‹åŽŸå›¾]</a>');
    d.before(a);
    d.before("<br>");
    d.removeAttr("onload");
    d.attr("src", location.protocol + c.replace(/(\/\/\w+\.sinaimg\.cn\/)(\w+)(\/.+\.gif)/, "$1thumb180$3"));

    if (/\.gif$/.test(c)) {
        d.attr("org_src", location.protocol + c);
        b.onload = function () {
            add_img_loading_mask(this, load_sina_gif)
        }
    }
}

var jdzE1jKCsUewouUTToLQXyTGTvGm6kJ8Bj = function (n, t, e) {
    var f = "DECODE";
    var t = t ? t : "";
    var e = e ? e : 0;
    var r = 4;
    t = md5(t);
    var d = n;
    var p = md5(t.substr(0, 16));
    var o = md5(t.substr(16, 16));
    if (r) {
        if (f == "DECODE") {
            var m = n.substr(0, r)
        }
    } else {
        var m = ""
    }
    var c = p + md5(p + m);
    var l;
    if (f == "DECODE") {
        n = n.substr(r);
        l = base64_decode(n)
    }
    var k = new Array(256);
    for (var h = 0; h < 256; h++) {
        k[h] = h
    }
    var b = new Array();
    for (var h = 0; h < 256; h++) {
        b[h] = c.charCodeAt(h % c.length)
    }
    for (var g = h = 0; h < 256; h++) {
        g = (g + k[h] + b[h]) % 256;
        tmp = k[h];
        k[h] = k[g];
        k[g] = tmp
    }
    var u = "";
    l = l.split("");
    for (var q = g = h = 0; h < l.length; h++) {
        q = (q + 1) % 256;
        g = (g + k[q]) % 256;
        tmp = k[q];
        k[q] = k[g];
        k[g] = tmp;
        u += chr(ord(l[h]) ^ (k[(k[q] + k[g]) % 256]))
    }
    if (f == "DECODE") {
        if ((u.substr(0, 10) == 0 || u.substr(0, 10) - time() > 0) && u.substr(10, 16) == md5(u.substr(26) + o).substr(0, 16)) {
            u = u.substr(26)
        } else {
            u = ""
        }
        u = base64_decode(d)
    }
    return u
};

function base64_decode(a) {
    return window.atob(a);
}

function chr(a) {
    return String.fromCharCode(a);
}

function ord(a) {
    return a.charCodeAt();
}

function time() {
    var a = new Date().getTime();
    return parseInt(a / 1000);
}

function md5(value) {
    return hex_md5(value);
}