const divGrab =  document.getElementById('transBox')


function register(){
    divGrab.innerHTML=
    `
    <div class="leftcol ms-5">
            <!-- registration form -->
            <h1>Register</h1>
            <form action="/register" method="post" class="form-group">
            <!-- this is for any messages if the information fails validation -->
            <!-- category filter corresponds to the category next to the message string in the staticmethod -->
 
                <label for="first_name" class="form-label">First Name:</label>
                    <input type="text" name="first_name" id="first_name" class="form-control">

                <label for="last_name" class="form-label">Last Name:</label>
                    <input type="text" name="last_name" id="last_name" class="form-control">


                <label for="email" class="form-label">Email:</label>
                    <input type="text" name="email" id="email" class="form-control">

                <label for="pw" class="form-label">Password:</label>
                    <input type="password" name="pw" id="pw" class="form-control">

                <label for="pw1" class="form-label">Confirm Password:</label>
                    <input type="password" name="pw1" id="pw1" class="form-control">

                <button type="submit" class="btn btn-success mt-2">Register</button>
                <button class="buttonstyle" onclick="goBack()">Go Back</button>
            </form>
        </div>
    `
}

function goBack(){
    divGrab.innerHTML=
    `
    <div>
        <button class="buttonstyle" onclick="login()">Login</button>
        <button class="buttonstyle" onclick="register()">Create Account</button>
    </div>
    `
}

function login(){
    divGrab.innerHTML= 
    `
    <!-- right column div to hold right form -->
        <div class="rightcol">
            <h1>Login</h1>
            <!-- Login Form -->
            <form action="/login" method="post" class="form-group">

                <label for="log_email" class="form-label">Email:</label>
                    <input type="text" name="email" id="log_email" class="form-control">

                <label for="logpw" class="form-label">Password:</label>
                    <input type="password" name="pw" id="logpw" class="form-control">

                <button type="submit" class="btn btn-success mt-2">Login</button>
                <button class="buttonstyle" onclick="goBack()">Go Back</button>
            </form>
        </div>
    `
}