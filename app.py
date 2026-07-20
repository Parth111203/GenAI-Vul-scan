from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)


HTML = """

<!DOCTYPE html>
<html>

<head>

<title>Cyber Recon Scanner</title>

<style>

body{
    background:#000;
    color:#00ff41;
    font-family:'Courier New', monospace;
    padding:30px;
}


.container{

    max-width:900px;
    margin:auto;

}


h1{

    text-align:center;
    font-size:40px;
    text-shadow:0 0 10px #00ff41;

}


.subtitle{

    text-align:center;
    color:#00aaaa;
}


.card{

    border:1px solid #00ff41;
    padding:25px;
    border-radius:10px;
    box-shadow:0 0 20px #00ff41;

}


input{

    width:70%;
    padding:15px;
    background:black;
    color:#00ff41;
    border:1px solid #00ff41;
    font-size:18px;

}


button{

    padding:15px 30px;
    background:#00ff41;
    color:black;
    border:none;
    font-weight:bold;
    cursor:pointer;
    font-size:16px;

}


button:hover{

    background:black;
    color:#00ff41;
    border:1px solid #00ff41;

}


.terminal{

    margin-top:30px;
    background:#050505;
    border:1px solid #00ff41;
    padding:20px;
    height:450px;
    overflow:auto;
    white-space:pre-wrap;

}


.status{

    color:#00ffff;

}


.footer{

    text-align:center;
    margin-top:20px;
    color:#777;

}


</style>


</head>



<body>


<div class="container">


<h1>
☠ CYBER RECON SCANNER ☠
</h1>


<p class="subtitle">
Automated Website Vulnerability Assessment Tool
</p>



<div class="card">


<form method="POST">


<p>
root@scanner:~$ Enter Target Domain
</p>


<input 
type="text"
name="domain"
placeholder="example.com"
required>


<button>
START SCAN
</button>


</form>


</div>




<div class="terminal">

{% if result %}

{{result}}

{% else %}

Waiting for target...

_

{% endif %}


</div>




<p class="footer">

Powered by Nmap | Curl | OpenSSL | WHOIS

</p>


</div>



</body>

</html>

"""



@app.route("/", methods=["GET","POST"])
def home():

    result=""


    if request.method=="POST":

        domain=request.form["domain"]


        result="[*] Initializing scan...\n\n"


        scan=subprocess.getoutput(
            f"bash vul-scanner.sh {domain}"
        )


        result += scan



    return render_template_string(
        HTML,
        result=result
    )



if __name__=="__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
