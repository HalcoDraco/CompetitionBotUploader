// Labels and constants
health_label = document.getElementById("healthConfig");
shield_label = document.getElementById("shieldConfig");
attack_label = document.getElementById("attackConfig");
health = 0;
shield = 0;
attack = 0;

error_label = document.getElementById("error_span");
error = "No status";

position_label = document.getElementById("position_span");
error_status_label = document.getElementById("error_status_span");
date_label = document.getElementById("date_span");
position = -1;
error_status = false;
date = "00/00/0000 00:00:00";

// Load previous data from server and update labels and information
if (download_config() && download_error_log() && download_user_info() != "") {
  // If all data could be loaded successfully, update labels
  showMessage("Your information has been loaded successfully.", false);
}
else {
  // If not, show error message
  showMessage("Your information couldn't be loaded. Please refresh the page or input the information again. ", true);
}



// FUNCTIONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function update_config(successful_download) {
  if (successful_download) {
    health_label.innerHTML = health;
    shield_label.innerHTML = shield;
    attack_label.innerHTML = attack;
  }
  else {
    health_label.innerHTML = "?";
    shield_label.innerHTML = "?";
    attack_label.innerHTML = "?";
  }
}

function update_error_log(successful_download) {
  if (successful_download) {
    error_label.innerHTML = error;
    error_label.style.color = "red";
  }
  else {
    error_label.innerHTML = "Couldn't load the log.";
    error_label.style.color = "red";
  }
}

function update_user_info(successful_download) {
  if (successful_download) {
    position_label.innerHTML = position;
    error_status_label.innerHTML = error_status;
    date_label.innerHTML = date;
  }
  else {
    position_label.innerHTML = "-1";
    error_status_label.innerHTML = "false";
    date_label.innerHTML = "00/00/0000 00:00:00";
  }
}
  

// BUTTONS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function log_button() {
  expand_form('75%')
  button = document.getElementById("log_button");
  if (button.innerHTML !== "Hide log") {
    button.innerHTML = "Hide log";
  }
  else {
    button.innerHTML = "Show last error log";
  }
}

// DOWNLOAD CONFIG AND INFO --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
async function download_config() {

  const response = await fetch('/download_config').then(response => response);
  const responseData = await response.json();
      
  if (response.ok) {

    health = responseData.health;
    shield = responseData.shield;
    attack = responseData.attack;
    
    update_config(true);
  
    return true;

  }
  else {

    update_config(false);

    return false;

  }
}

async function download_error_log() {

  const response = await fetch('/download_error_log').then(response => response);
  const responseData = await response.json();
      
  if (response.ok) {
    // Load data
    error_log = responseData.error_log;

    update_error_log(true);

    return true;

  } 
  else {
    update_error_log(false);
    return false;
  }
}

async function download_user_info() {

  const response = await fetch('/download_user_info').then(response => response);
  const responseData = await response.json();
      
  if (response.ok) {
    // Load data
    position = responseData.position;
    error_status = responseData.error_status;
    date = responseData.date;

    update_user_info(true);

    return true;

  } 
  else {
    update_user_info(false);
    return false;
  }
}