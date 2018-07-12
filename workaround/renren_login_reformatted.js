function isCapsLockOn(e) {
    var i = e.keyCode || e.which
      , t = e.shiftKey;
    return i >= 65 && 90 >= i && !t || i >= 97 && 122 >= i && t ? !0 : !1
}
function showMsg(e) {
    console.log(e);
    var i = $("errorMessage");
    i && (i.style.display = "block",
    i.innerHTML = e)
}
function hideMsg() {
    $("errorMessage") && ($("errorMessage").style.display = "none");
    for (var e = Sizzle("dd"), i = 0; i < e.length; i++)
        (e[i].style.backgroundColor = "#FFFFD9") && (e[i].style.backgroundColor = "")
}
function showCapsLockMsg(e) {
    var i = $("capsLockMessage");
    i && (i.visible() || (i.style.display = "block",
    i._hidetimer && (clearTimeout(i._hidetimer),
    i._hidetimer = null),
    i._hidetimer = setTimeout(function() {
        i.style.display = "none"
    }, 3e3)))
}
function hideCapsLockMsg() {
    $("capsLockMessage") && ($("capsLockMessage").style.display = "none")
}
function refreshCode_login() {
    var e = $("verifyPic_login");
    e.src = e.src.split("&")[0] + "&rnd=" + Math.random()
}
function closeError() {
    $("yellow_error").style.display = "none"
}
function closeStop() {
    $("account_stop").style.display = "none"
}
function closeLock() {
    $("account_lock").style.display = "none"
}
function showCode() {
    var e = $("code")
      , i = $("codeimg")
      , t = $("email");
    new XN.net.xmlhttp({
        url: "http://www.renren.com/ajax/ShowCaptcha",
        data: "email=" + t.value,
        method: "post",
        onSuccess: function(t) {
            0 == t.responseText ? (e.style.display = "none",
            i.style.display = "none") : (e.style.display = "block",
            i.style.display = "block",
            $("regnow").style.marginTop = "88px",
            document.querySelector(".regnow").style.zIndex = "-1")
        },
        onError: function() {
            XN.DO.showError("网络通信失败，请稍后再试！")
        }
    })
}
object.define("cryption", "net, dom", function(require, e) {
    function t(e, i, t) {
        this.e = m(e),
        this.d = m(i),
        this.m = m(t),
        this.chunkSize = 2 * N(this.m),
        this.radix = 16,
        this.barrett = new o(this.m)
    }
    function n(e, i) {
        for (var t = new Array, n = i.length, o = 0; n > o; )
            t[o] = i.charCodeAt(o),
            o++;
        for (; t.length % e.chunkSize != 0; )
            t[o++] = 0;
        var s, r, a, l = t.length, c = "";
        for (o = 0; l > o; o += e.chunkSize) {
            for (a = new d,
            s = 0,
            r = o; r < o + e.chunkSize; ++s)
                a.digits[s] = t[r++],
                a.digits[s] += t[r++] << 8;
            var u = e.barrett.powMod(a, e.e)
              , g = 16 == e.radix ? p(u) : f(u, e.radix);
            c += g + " "
        }
        return c.substring(0, c.length - 1)
    }
    function o(e) {
        this.modulus = c(e),
        this.k = N(this.modulus) + 1;
        var i = new d;
        i.digits[2 * this.k] = 1,
        this.mu = S(i, this.modulus),
        this.bkplus1 = new d,
        this.bkplus1.digits[this.k + 1] = 1,
        this.modulo = s,
        this.multiplyMod = r,
        this.powMod = a
    }
    function s(e) {
        var i = X(e, this.k - 1)
          , t = C(i, this.mu)
          , n = X(t, this.k + 1)
          , o = D(e, this.k + 1)
          , s = C(n, this.modulus)
          , r = D(s, this.k + 1)
          , a = b(o, r);
        a.isNeg && (a = w(a, this.bkplus1));
        for (var l = L(a, this.modulus) >= 0; l; )
            a = b(a, this.modulus),
            l = L(a, this.modulus) >= 0;
        return a
    }
    function r(e, i) {
        var t = C(e, i);
        return this.modulo(t)
    }
    function a(e, i) {
        var t = new d;
        t.digits[0] = 1;
        for (var n = e, o = i; ; ) {
            if (0 != (1 & o.digits[0]) && (t = this.multiplyMod(t, n)),
            o = E(o, 1),
            0 == o.digits[0] && 0 == N(o))
                break;
            n = this.multiplyMod(n, n)
        }
        return t
    }
    function l(e) {
        B = e,
        z = new Array(B);
        for (var i = 0; i < z.length; i++)
            z[i] = 0;
        O = new d,
        I = new d,
        I.digits[0] = 1
    }
    function d(e) {
        "boolean" == typeof e && 1 == e ? this.digits = null : this.digits = z.slice(0),
        this.isNeg = !1
    }
    function c(e) {
        var i = new d(!0);
        return i.digits = e.digits.slice(0),
        i.isNeg = e.isNeg,
        i
    }
    function u(e) {
        var i = new d;
        i.isNeg = 0 > e,
        e = Math.abs(e);
        for (var t = 0; e > 0; )
            i.digits[t++] = e & H,
            e >>= P;
        return i
    }
    function g(e) {
        for (var i = "", t = e.length - 1; t > -1; --t)
            i += e.charAt(t);
        return i
    }
    function f(e, i) {
        var t = new d;
        t.digits[0] = i;
        for (var n = A(e, t), o = Q[n[1].digits[0]]; 1 == L(n[0], O); )
            n = A(n[0], t),
            digit = n[1].digits[0],
            o += Q[n[1].digits[0]];
        return (e.isNeg ? "-" : "") + g(o)
    }
    function v(e) {
        var t = 15
          , n = "";
        for (i = 0; i < 4; ++i)
            n += Z[e & t],
            e >>>= 4;
        return g(n)
    }
    function p(e) {
        for (var i = "", t = (N(e),
        N(e)); t > -1; --t)
            i += v(e.digits[t]);
        return i
    }
    function h(e) {
        var i, t = 48, n = t + 9, o = 97, s = o + 25, r = 65, a = 90;
        return i = e >= t && n >= e ? e - t : e >= r && a >= e ? 10 + e - r : e >= o && s >= e ? 10 + e - o : 0
    }
    function y(e) {
        for (var i = 0, t = Math.min(e.length, 4), n = 0; t > n; ++n)
            i <<= 4,
            i |= h(e.charCodeAt(n));
        return i
    }
    function m(e) {
        for (var i = new d, t = e.length, n = t, o = 0; n > 0; n -= 4,
        ++o)
            i.digits[o] = y(e.substr(Math.max(n - 4, 0), Math.min(n, 4)));
        return i
    }
    function w(e, i) {
        var t;
        if (e.isNeg != i.isNeg)
            i.isNeg = !i.isNeg,
            t = b(e, i),
            i.isNeg = !i.isNeg;
        else {
            t = new d;
            for (var n, o = 0, s = 0; s < e.digits.length; ++s)
                n = e.digits[s] + i.digits[s] + o,
                t.digits[s] = 65535 & n,
                o = Number(n >= K);
            t.isNeg = e.isNeg
        }
        return t
    }
    function b(e, i) {
        var t;
        if (e.isNeg != i.isNeg)
            i.isNeg = !i.isNeg,
            t = w(e, i),
            i.isNeg = !i.isNeg;
        else {
            t = new d;
            var n, o;
            o = 0;
            for (var s = 0; s < e.digits.length; ++s)
                n = e.digits[s] - i.digits[s] + o,
                t.digits[s] = 65535 & n,
                t.digits[s] < 0 && (t.digits[s] += K),
                o = 0 - Number(0 > n);
            if (-1 == o) {
                o = 0;
                for (var s = 0; s < e.digits.length; ++s)
                    n = 0 - t.digits[s] + o,
                    t.digits[s] = 65535 & n,
                    t.digits[s] < 0 && (t.digits[s] += K),
                    o = 0 - Number(0 > n);
                t.isNeg = !e.isNeg
            } else
                t.isNeg = e.isNeg
        }
        return t
    }
    function N(e) {
        for (var i = e.digits.length - 1; i > 0 && 0 == e.digits[i]; )
            --i;
        return i
    }
    function k(e) {
        var i, t = N(e), n = e.digits[t], o = (t + 1) * q;
        for (i = o; i > o - q && 0 == (32768 & n); --i)
            n <<= 1;
        return i
    }
    function C(e, i) {
        for (var t, n, o, s = new d, r = N(e), a = N(i), l = 0; a >= l; ++l) {
            for (t = 0,
            o = l,
            j = 0; j <= r; ++j,
            ++o)
                n = s.digits[o] + e.digits[j] * i.digits[l] + t,
                s.digits[o] = n & H,
                t = n >>> P;
            s.digits[l + r + 1] = t
        }
        return s.isNeg = e.isNeg != i.isNeg,
        s
    }
    function $(e, i) {
        var t, n, o;
        result = new d,
        t = N(e),
        n = 0;
        for (var s = 0; t >= s; ++s)
            o = result.digits[s] + e.digits[s] * i + n,
            result.digits[s] = o & H,
            n = o >>> P;
        return result.digits[1 + t] = n,
        result
    }
    function x(e, i, t, n, o) {
        for (var s = Math.min(i + o, e.length), r = i, a = n; s > r; ++r,
        ++a)
            t[a] = e[r]
    }
    function F(e, i) {
        var t = Math.floor(i / q)
          , n = new d;
        x(e.digits, 0, n.digits, t, n.digits.length - t);
        for (var o = i % q, s = q - o, r = n.digits.length - 1, a = r - 1; r > 0; --r,
        --a)
            n.digits[r] = n.digits[r] << o & H | (n.digits[a] & J[o]) >>> s;
        return n.digits[0] = n.digits[r] << o & H,
        n.isNeg = e.isNeg,
        n
    }
    function E(e, i) {
        var t = Math.floor(i / q)
          , n = new d;
        x(e.digits, t, n.digits, 0, e.digits.length - t);
        for (var o = i % q, s = q - o, r = 0, a = r + 1; r < n.digits.length - 1; ++r,
        ++a)
            n.digits[r] = n.digits[r] >>> o | (n.digits[a] & W[o]) << s;
        return n.digits[n.digits.length - 1] >>>= o,
        n.isNeg = e.isNeg,
        n
    }
    function M(e, i) {
        var t = new d;
        return x(e.digits, 0, t.digits, i, t.digits.length - i),
        t
    }
    function X(e, i) {
        var t = new d;
        return x(e.digits, i, t.digits, 0, t.digits.length - i),
        t
    }
    function D(e, i) {
        var t = new d;
        return x(e.digits, 0, t.digits, 0, i),
        t
    }
    function L(e, i) {
        if (e.isNeg != i.isNeg)
            return 1 - 2 * Number(e.isNeg);
        for (var t = e.digits.length - 1; t >= 0; --t)
            if (e.digits[t] != i.digits[t])
                return e.isNeg ? 1 - 2 * Number(e.digits[t] > i.digits[t]) : 1 - 2 * Number(e.digits[t] < i.digits[t]);
        return 0
    }
    function A(e, i) {
        var t, n, o = k(e), s = k(i), r = i.isNeg;
        if (s > o)
            return e.isNeg ? (t = c(I),
            t.isNeg = !i.isNeg,
            e.isNeg = !1,
            i.isNeg = !1,
            n = b(i, e),
            e.isNeg = !0,
            i.isNeg = r) : (t = new d,
            n = c(e)),
            new Array(t,n);
        t = new d,
        n = e;
        for (var a = Math.ceil(s / q) - 1, l = 0; i.digits[a] < R; )
            i = F(i, 1),
            ++l,
            ++s,
            a = Math.ceil(s / q) - 1;
        n = F(n, l),
        o += l;
        for (var u = Math.ceil(o / q) - 1, g = M(i, u - a); -1 != L(n, g); )
            ++t.digits[u - a],
            n = b(n, g);
        for (var f = u; f > a; --f) {
            var v = f >= n.digits.length ? 0 : n.digits[f]
              , p = f - 1 >= n.digits.length ? 0 : n.digits[f - 1]
              , h = f - 2 >= n.digits.length ? 0 : n.digits[f - 2]
              , y = a >= i.digits.length ? 0 : i.digits[a]
              , m = a - 1 >= i.digits.length ? 0 : i.digits[a - 1];
            v == y ? t.digits[f - a - 1] = H : t.digits[f - a - 1] = Math.floor((v * K + p) / y);
            for (var C = t.digits[f - a - 1] * (y * K + m), x = v * U + (p * K + h); C > x; )
                --t.digits[f - a - 1],
                C = t.digits[f - a - 1] * (y * K | m),
                x = v * K * K + (p * K + h);
            g = M(i, f - a - 1),
            n = b(n, $(g, t.digits[f - a - 1])),
            n.isNeg && (n = w(n, g),
            --t.digits[f - a - 1])
        }
        return n = E(n, l),
        t.isNeg = e.isNeg != r,
        e.isNeg && (t = r ? w(t, I) : b(t, I),
        i = E(i, l),
        n = b(i, n)),
        0 == n.digits[0] && 0 == N(n) && (n.isNeg = !1),
        new Array(t,n)
    }
    function S(e, i) {
        return A(e, i)[0]
    }
    var _ = (require("dom"),
    require("net"))
      , T = null;
    e.getKeys = function(e, i) {
        var n = this;
        n.getKeys = function() {
            var e = new _.Request({
                url: "http://login.renren.com/ajax/getEncryptKey",
                onSuccess: function(e) {
                    var n = JSON.parse(e.responseText);
                    1 == n.isEncrypt && (l(2 * n.maxdigits),
                    T = new t(n.e,"null",n.n),
                    XN.isFunction(i) && i.call(this, T, n.rkey))
                },
                onError: function() {
                    XN.DO.showError("网络通信失败，请稍后再试！")
                }
            });
            e.send()
        }
        ,
        n.getKeys()
    }
    ,
    e.encrypt = function(e, i) {
        encrypted = n(T, e),
        i(encrypted)
    }
    ;
    var B, z, O, I, P = 16, q = P, K = 65536, R = K >>> 1, U = K * K, H = K - 1;
    l(20);
    var Q = (u(1e15),
    new Array("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"))
      , Z = new Array("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f")
      , J = new Array(0,32768,49152,57344,61440,63488,64512,65024,65280,65408,65472,65504,65520,65528,65532,65534,65535)
      , W = new Array(0,1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535)
}),
object.define("login/cryption", "string, dom, net, cryption", function(require, e) {
    function i(e) {
        try {} catch (i) {}
    }
    function t(e, t, n, o) {
        void 0 != e && null != e && (e += -1 == e.indexOf("?") ? "?1=1" : "&1=1");
        try {
            var s = new Date;
            e = e + "&uniqueTimestamp=" + s.getFullYear() + s.getMonth() + s.getDay() + s.getHours() + s.getSeconds() + s.getUTCMilliseconds()
        } catch (r) {}
        var d = XN.form.getElements("loginForm");
        "" != u && (d = d.filter(function(e, i) {
            return "password" != e.name
        }));
        var c = XN.form.serializeElements(d, "string");
        c += "&" + l.toQueryString(t);
        var g = new a.Request({
            url: e,
            method: "post",
            onSuccess: function(e) {
                if (n) {
                    var t = JSON.parse(e.responseText);
                    n(t)
                } else
                    i()
            },
            onError: function() {
                XN.DO.showError("网络通信失败，请稍后再试！")
            }
        });
        g.send(c)
    }
    function n() {
        define(function(require) {
            require("ui/dialog");
            var e = require("jquery")
              , i = '<div>                            <p class="login-dialog-title"><span class="ui-icon ui-icon-failure"></span> 您的帐号由于以下某种原因需要解锁才能登录</p>                            <ul class="login-dialog-list">                                <li>删除过帐号</li>                                <li>长时间没有登录网站</li>                                <li>安全原因</li>                            </ul>                        </div>';
            e.ui.dialog({
                dialogClass: "dialog-login-error",
                width: 500,
                height: 250,
                buttons: [{
                    text: "取消",
                    click: function() {
                        var i = e(this).dialog("instance");
                        i._trigger("cancel"),
                        i.close()
                    }
                }, {
                    text: "立即解锁",
                    "class": "ui-button-blue",
                    click: function() {
                        window.open("http://safe.renren.com/relive.do", "_blank")
                    }
                }]
            }, e(i))
        })
    }
    function o() {
        define(function(require) {
            require("ui/dialog");
            var e = require("jquery")
              , i = '<div>                            <p class="login-dialog-title"><span class="ui-icon ui-icon-failure"></span> 您的帐号已停止使用，如有疑问请联系客服</p>                        </div>';
            e.ui.dialog({
                dialogClass: "dialog-login-error",
                width: 500,
                height: 200,
                buttons: [{
                    text: "取消",
                    click: function() {
                        var i = e(this).dialog("instance");
                        i._trigger("cancel"),
                        i.close()
                    }
                }, {
                    text: "联系客服",
                    "class": "ui-button-blue",
                    click: function() {
                        window.open("http://help.renren.com/#http://help.renren.com/support/contomvice?pid=2&selection={couId:193,proId:342,cityId:1000375}", "_blank")
                    }
                }]
            }, e(i))
        })
    }
    function s() {
        var e, i = $("errorMessage"), s = $("codeTip"), r = $("code"), a = $("codeimg"), l = ($("forgetPwd"),
        $("getpassword"),
        $("account_stop"),
        $("account_lock"),
        $("password")), d = $("email"), g = $("sendemail"), f = $("yellow_error"), v = $("gotoEmail");
        e = "" != u ? {
            password: c,
            rkey: u
        } : {},
        e.f = encodeURIComponent(document.referrer),
        t("http://www.renren.com/ajaxLogin/login", e, function(e) {
            1 == e.code ? window.location.href = e.homeUrl : (i.style.display = "block",
            s.style.visibility = "visible",
            showMsg(e.failDescription),
            e.catchaCount > 2 && (r.style.display = "block",
            a.style.display = "block",
            $("regnow").style.marginTop = "88px",
            document.querySelector(".regnow").style.zIndex = "-1",
            e.catchaCount > 4 && 4 == e.failCode && e.emailLoginUrl && (g.innerHTML = e.email,
            f.style.display = "block",
            "block" == r.style.display && (f.style.height = "310px"),
            v.href = e.emailLoginUrl,
            XN.event.addEvent(v, "click", function() {
                f.style.display = "none"
            }))),
            1 == e.failCode || 2 == e.failCode || 4 == e.failCode || 128 == e.failCode ? (d.parentNode.style.backgroundColor = "#FFFFD9",
            l.parentNode.style.backgroundColor = "#FFFFD9",
            l.value = "",
            Sizzle("#code .input-text")[0].value = "",
            l.focus()) : 512 == e.failCode ? (r.style.display = "block",
            a.style.display = "block",
            r.getElementsByTagName("dd")[0].style.backgroundColor = "#FFFFD9",
            Sizzle("#code .input-text")[0].value = "",
            s.style.visibility = "hidden") : 64 == e.failCode ? (n(),
            s.style.visibility = "hidden") : 16 == e.failCode && (o(),
            s.style.visibility = "hidden"),
            refreshCode_login())
        })
    }
    var r = require("cryption")
      , a = require("net")
      , l = (require("dom"),
    require("string"))
      , d = ""
      , c = ""
      , u = "";
    window.getKeys = function() {
        r.getKeys("key.jsp?generateKeypair=true", function(e, i) {
            u = i
        })
    }
    ,
    $("loginForm") && ($("loginForm").onsubmit = function() {
        function e(e) {
            var t = "";
            e = e.replace(/^\s+|\s+$/g, "");
            for (var n = 0, o = e.length; o > n; n++) {
                var s = e.charCodeAt(n);
                t += s >= 65281 && 65373 >= s ? String.fromCharCode(s - 65248) : String.fromCharCode(s)
            }
            return t = t.replace(/·/, "@"),
            i = t = t.replace(/[。|,|，|、]/g, "."),
            /^[A-Z_a-z0-9-\.]+@([A-Z_a-z0-9-]+\.)+[a-z0-9A-Z]{2,4}$/.test(t)
        }
        var i = $("email").value.trim()
          , t = $("password").value.trim()
          , n = $("email")
          , o = $("password");
        if (null == i || "" == i || "邮箱/手机号/用户名" == i)
            return showMsg("请输入用户名和密码"),
            n.focus(),
            n.parentNode.style.backgroundColor = "#FFFFD9",
            !1;
        if (/^\s*$/.test(t))
            return showMsg("您还没有填写密码"),
            o.focus(),
            o.parentNode.style.backgroundColor = "#FFFFD9",
            !1;
        if (/@/.test(i)) {
            if (!e(i))
                return showMsg("E-mail格式错误"),
                n.focus(),
                n.parentNode.style.backgroundColor = "#FFFFD9",
                !1
        } else if (!/^[\w@_.-]{3,50}$/.test(i))
            return showMsg("帐号格式错误"),
            n.focus(),
            n.parentNode.style.backgroundColor = "#FFFFD9",
            !1;
        return "" != u ? r.encrypt(i, function(e) {
            d = e,
            setTimeout(function() {
                r.encrypt(t, function(e) {
                    c = e,
                    s()
                })
            }, 0)
        }) : s(),
        !1
    }
    )
}),
function() {
    window.XN || (XN = {}),
    XN.Browser || (XN.Browser = XN.BORWSER = {}),
    XN.Browser.addHomePage = function(e) {
        if (window.attachEvent && !window.opera)
            document.body.style.behavior = "url(#default#homepage)",
            document.body.setHomePage(e);
        else {
            if (!window.clipboardData || !clipboardData.setData)
                return void alert("您的浏览器不允许脚本访问剪切板，请手动设置~");
            clipboardData.setData("text", e),
            alert("网址已经拷贝到剪切板,请您打开浏览器的选项,\n把地址粘到主页选项中即可~")
        }
        return !0
    }
    ,
    XN.Browser.addBookMark = function(e, i) {
        var t = -1 != navigator.userAgent.toLowerCase().indexOf("mac") ? "Command/Cmd" : "CTRL";
        try {
            window.external.addFavorite(e, i || "" + XN.env.siteName + "-因为真实,所以精彩")
        } catch (n) {
            try {
                window.sidebar.addPanel(e, i || "" + XN.env.siteName + "-因为真实,所以精彩")
            } catch (n) {
                alert("您可以尝试通过快捷键" + t + " + D 添加书签~")
            }
        }
    }
}(),
$("email").onkeypress = function() {
    hideMsg()
}
,
$("password").onkeypress = function(e) {
    hideMsg(),
    isCapsLockOn(e || window.event) ? showCapsLockMsg("大写锁定开启") : hideCapsLockMsg()
}
,
$("password").onblur = function(e) {
    hideCapsLockMsg()
}
,
object.use("login/cryption, dom", function(e, i) {
    XN.dom.ready(function() {
        function e(e) {
            var i = e.width / e.height;
            k = F,
            C = k / i,
            C >= E ? e.style.marginTop = -(C - E) / 2 + "px" : (C = E,
            k = C * i,
            e.style.marginLeft = -(k - F) / 2 + "px"),
            e.width = k,
            e.height = C
        }
        var t = $("email")
          , n = $("password")
          , o = "邮箱/手机号/用户名"
          , s = $("pwdTip")
          , r = ($("forgetPwd"),
        $("getpassword"),
        $("icode"))
          , a = $("codeTip")
          , l = $("code")
          , d = $("codeimg")
          , c = $("account_stop")
          , u = $("account_lock")
          , g = $("errorMessage");
        if (i.getElements(".intro .item").addEvent("mouseover", function() {
            var e = this;
            XN.element.delClass(e, "unactive"),
            XN.element.addClass(e, "active")
        }),
        i.getElements(".intro .item").addEvent("mouseleave", function() {
            var e = this;
            XN.element.delClass(e, "active"),
            XN.element.addClass(e, "unactive")
        }),
        "" == t.value || t.value == o) {
            navigator.userAgent.toLowerCase().indexOf("firefox") > 0 && navigator.userAgent.toLowerCase().indexOf("macintosh") > 0 ? t.value = o : (t.focus(),
            t.value = o,
            t.select()),
            new XN.FORM.inputHelper(t).setDefaultValue(o),
            XN.event.addEvent(t, "click", function() {
                t.value == o && (t.value = "",
                t.style.color = "#333")
            }),
            XN.event.addEvent(t, "blur", function() {
                t.value == o && (t.style.color = "#888")
            });
            var f = setInterval(function() {
                "" != t.value && t.value != o && (t.style.color = "#333",
                clearInterval(f))
            }, 100)
        } else
            n.focus();
        XN.event.addEvent(t, "focus", function() {
            t.parentNode.style.borderColor = "#8E96A1";
            var e = setInterval(function() {
                "" != n.value && (s.style.visibility = "hidden",
                clearInterval(e))
            }, 100)
        });
        var v, p = document.cookie;
        v = p.split(";");
        for (var h, y, m = 0, w = v.length; w > m; m++) {
            if (y = jxn.trim(v[m]),
            h = y.split("="),
            "ln_hurl" == jxn.trim(h[0]))
                var b = decodeURIComponent(jxn.trim(h[1]));
            if ("ln_uact" == jxn.trim(h[0]))
                var N = decodeURIComponent(jxn.trim(h[1]));
            console.log(h)
        }
        if (b && N) {
            $("personhead").src = b,
            console.log(N),
            $("email").value = N;
            var k, C, x = $("personhead"), F = 100, E = 100;
            x.complete ? e(x) : x.onload = function() {
                e(x)
            }
        } else
            $("personhead").src = "http://a.xnimg.cn/nx/apps/login/cssimg/person.jpg";
        $("password").onclick = function() {
            $("password").type = "password"
        }
        ;
        $("email").onkeyup = function() {
            $("personhead").src = "http://a.xnimg.cn/nx/apps/login/cssimg/person.jpg"
        }
        ;
        var M = Sizzle(".qrcode")[0];
        XN.event.addEvent(M, "click", function() {
            define(function(require) {
                require.async("ui/dialog", function() {
                    function e(i) {
                        t.uiDialog.has(i.target).length || i.target === M || (t.close(),
                        jQuery("body").off("click", e))
                    }
                    var i = '<div style="padding: 10px;text-align: center"><img src="http://a.xnimg.cn/nx/apps/login/res/down-qr.jpg" /><p>扫描二维码下载人人手机客户端</p></div>'
                      , t = jQuery.ui.dialog({
                        width: XN.browser.IE ? 170 : 190,
                        buttons: [],
                        modal: !1,
                        position: {
                            my: "center",
                            at: "center",
                            of: jQuery(M),
                            collision: "flip"
                        }
                    }, jQuery(i));
                    setTimeout(function() {
                        t.uiDialogTitlebar.hide()
                    }, 0),
                    jQuery("body").on("click", e)
                })
            })
        }),
        XN.event.addEvent(t, "blur", function() {
            var e = t.value;
            null != e && "" != e && "邮箱/手机号/用户名" != e && showCode(),
            t.parentNode.style.borderColor = "#ADB6C9"
        }),
        XN.event.addEvent(n, "focus", function() {
            s.style.visibility = "hidden"
        }),
        XN.event.addEvent(n, "blur", function() {
            "" == n.value && (s.style.visibility = "visible")
        });
        var j = setInterval(function() {
            "" != n.value && (s.style.visibility = "hidden",
            clearInterval(j))
        }, 100);
        if (XN.event.addEvent(n, "focus", function() {
            n.parentNode.style.borderColor = "#8E96A1"
        }),
        XN.event.addEvent(n, "blur", function() {
            n.parentNode.style.borderColor = "#ADB6C9"
        }),
        XN.event.addEvent(r, "blur", function() {
            "" == r.value && (a.style.visibility = "visible"),
            r.parentNode.style.borderColor = "#ADB6C9"
        }),
        XN.event.addEvent(r, "focus", function() {
            r.parentNode.style.borderColor = "#8E96A1",
            a.style.visibility = "hidden",
            l.getElementsByTagName("dd")[0].style.backgroundColor = "#FFF"
        }),
        XN.event.addEvent($("autoLogin"), "focus", function() {
            i.wrap($("autoLogin").parentNode),
            $("autoLogin").parentNode.addClass("focuscheck")
        }),
        XN.event.addEvent($("autoLogin"), "blur", function() {
            i.wrap($("autoLogin").parentNode),
            $("autoLogin").parentNode.removeClass("focuscheck")
        }),
        $("autoLogin").addEvent("click", function(e) {
            $($("autoLogin").parentNode).toggleClass("not")
        }),
        window.location.href.indexOf("failCode") > 0) {
            g.style.display = "block";
            var X, D = +window.location.search.match(/failCode=(\d+)/)[1];
            switch (D) {
            case -1:
                X = "登录成功";
                break;
            case 0:
                X = "登录系统错误，请稍后尝试";
                break;
            case 1:
                X = "您的用户名和密码不匹配";
                break;
            case 2:
                X = "您的用户名和密码不匹配";
                break;
            case 4:
                X = "您的用户名和密码不匹配";
                break;
            case 8:
                X = "请输入帐号，密码";
                break;
            case 16:
                X = "您的帐号被停止使用";
                break;
            case 32:
                X = "帐号未激活，请激活帐号";
                break;
            case 64:
                X = "帐号已经注销";
                break;
            case 128:
                X = "您的用户名和密码不匹配";
                break;
            case 512:
                X = "请您输入验证码";
                break;
            case 4096:
                X = "登录系统错误，稍后尝试";
                break;
            case 8192:
                X = "您的用户名和密码不匹配";
                break;
            case 16384:
                X = "网络不给力，请稍候重试"
            }
            showMsg(X),
            catchaCount > 2 && (l.style.display = "block",
            d.style.display = "block"),
            64 == D ? u.style.display = "block" : 512 == D ? (l.style.display = "block",
            d.style.display = "block") : 16 == D ? c.style.display = "block" : (1 == D || 2 == D || 4 == D || 128 == D) && (t.parentNode.style.backgroundColor = "#FFFFD9",
            n.parentNode.style.backgroundColor = "#FFFFD9"),
            refreshCode_login()
        }
        var L = t.value;
        if (null != L && "" != L && "邮箱/手机号/用户名" != L && showCode(),
        getKeys(),
        document.createEvent) {
            var A = document.createEvent("HTMLEvents");
            A.initEvent("focus", !1, !0),
            n.dispatchEvent(A),
            t.dispatchEvent(A)
        }
    })
}),
function() {
    if ("undefined" != typeof homePreloadFiles) {
        var e = !1
          , i = function() {
            if (!e) {
                e = !0;
                for (var i = 0, t = homePreloadFiles.length; t > i; i++)
                    (new Image).src = homePreloadFiles[i]
            }
        };
        XN.dom.ready(function() {
            $("email").addEvent("focus", i),
            $("password").addEvent("focus", i),
            setTimeout(i, 3e3)
        })
    }
}(),
object.define("renren/core/ipadBanner", "jxn", function(require, e) {
    var i = jxn(".iPadDown")
      , t = function() {
        var e = n();
        e && s()
    }
      , n = function() {
        var e = "";
        if (navigator.userAgent.match(/iPad/i) && navigator.userAgent.match(/OS 6/i))
            e = "itms-apps://phobos.apple.com/WebObjects/MZStore.woa/wa/viewSoftware?id=455215726";
        else {
            if (!navigator.userAgent.match(/iPad/i) || !navigator.userAgent.match(/OS 7/i))
                return !1;
            e = "itms-apps://itunes.apple.com/app/id455215726"
        }
        return o(),
        jxn(".iUrl").attr("href", e),
        r(),
        a(),
        !0
    }
      , o = function() {
        if (0 == i.length) {
            var e = ['<div class="iPadDown">', '<a href="#" class="closeBtn"></a>', '<a href="#" class="iUrl">', '<img src="http://a.xnimg.cn/n/core/modules/ipadBanner/images/banner-width.png" class="iPadBg">', "</a>", "</div>"].join("");
            i = jxn(e),
            i.insertBefore(jxn("#navBar"))
        } else
            i.show();
        var t = jxn(".iPadBg")
          , n = jxn(window).width() + "px";
        t.css("width", n)
    }
      , s = function() {
        var e = jxn(".closeBtn");
        e.click(function() {
            var e = jxn("#navBar")
              , t = jxn(".site-nav-wrapper");
            i.hide(),
            t.css("height", "31px"),
            e.css("top", "0")
        })
    }
      , r = function() {
        var e = jxn("#navBar")
          , i = jxn(".site-nav-wrapper");
        i.css("height", "95px"),
        e.css("top", "64px")
    }
      , a = function() {
        jxn(".site-nav-wrapper").length > 0 && i.css("position", "fixed")
    };
    e.init = t
}),
XN.dom.ready(function() {
    object.use("renren/core/ipadBanner", function(e) {
        e.init()
    })
}),
define(function(require) {
    require("ui/dialog");
    var e = require("jquery")
      , i = {
        hideFocus: function() {
            var i = e(".login-recommend .content");
            i.each(function(e, i) {
                i.setAttribute("hideFocus", !0)
            })
        }
    }
      , t = function() {
        if (e(".login-superlarge").length) {
            var i = e("#ad100000000108")
              , t = e(window).width();
            if (t > 982 && 1440 > t) {
                i.width(t - 2).css("left", -(t - 982) / 2)
            }
        }
    };
    e(function() {
        for (var n in i)
            i[n]();
        t(),
        e(window).resize(function() {
            t()
        })
    })
});
