from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html>

<head>
<title>Vulnerability Assessment Dashboard</title>

<style>

body {
    background: #0f172a;
    color: #e2e8f0;
    font-family: Arial, sans-serif;
    margin: 0;
}


.header {
    background: #111827;
    padding: 25px;
    text-align: center;
    border-bottom: 1px solid #334155;
}


.header h1 {
    margin: 0;
    color: #38bdf8;
}


.header p {
    color: #94a3b8;
}


.container {
    width: 80%;
    margin: 30px auto;
}


.card {

    background: #1e293b;
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 25px;
    border:1px solid #334155;

}


label {

    display:block;
    margin-bottom:10px;
    color:#cbd5e1;

}


input {

    width:70%;
    padding:12px;
    background:#0f172a;
    color:white;
    border:1px solid #475569;
    border-radius:5px;
    font-size:16px;

}


button {

    padding:12px 25px;
    background:#0284c7;
    color:white;
    border:none;
    border-radius:5px;
    cursor:pointer;
    margin-left:10px;

}


button:hover {

    background:#0369a1;

}


.status {

    display:flex;
    gap:20px;

}


.box {

    flex:1;
    background:#0f172a;
    padding:20px;
    border-radius:8px;
    border:1px solid #334155;
}


.box h3 {

    color:#38bdf8;

}


.output {

    background:#020617;
    color:#22c55e;
    padding:20px;
    border-radius:8px;
    height:400px;
    overflow:auto;
    font-family:monospace;
    white-space:pre-wrap;

}


.footer {

    text-align:center;
    color:#64748b;
    padding:20px;

}

</style>


</head>


<body>


<div class="header">

<h1>Security Vulnerability Assessment Tool</h1>

<p>Automated Website Reconnaissance and Vulnerability Scanner</p>

</div>



<div class="container">


<div class="card">

<h2>Start Security Scan</h2>


<form method="POST">


<label>
Target Website
</label>


<input 
type="text"
name="domain"
placeholder="example.com"
required>


<button>
Run Scan
</button>


</form>


</div>




<div class="status">


<div class="box">

<h3>Scanner</h3>

<p>Active</p>

</div>


<div class="box">

<h3>Tools</h3>

<p>Nmap | Curl | OpenSSL | Whois</p>

</div>


<div class="box">

<h3>Mode</h3>

<p>Recon + Vulnerability Check</p>

</div>


</div>





<div class="card">


<h2>Scan Result</h2>


<div class="output">

{% if result %}

{{result}}

{% else %}

Waiting for scan...

{% endif %}


</div>


</div>



</div>



<div class="footer">

PGCP-ITISS Mini Project | Website Vulnerability Scanner

</div>



</body>

</html>

"""


@app.route("/", methods=["GET","POST"])
def home():

    result = ""


    if request.method == "POST":

        domain = request.form["domain"]


        try:

            result = subprocess.getoutput(
                f"bash vul-scanner.sh {domain}"
            )

        except Exception as e:

            result = str(e)



    return render_template_string(
        HTML,
        result=result
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
