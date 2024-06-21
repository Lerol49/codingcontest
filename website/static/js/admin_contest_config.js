function loadProblemsPage() {
  
  document.getElementById("participants_field").classList.add("hidden");
  document.getElementById("config_field").classList.add("hidden");

  document.getElementById("problem_field").classList.remove("hidden");
}


function loadParticipantsPage() {
  
  document.getElementById("problem_field").classList.add("hidden");
  document.getElementById("config_field").classList.add("hidden");

  document.getElementById("participants_field").classList.remove("hidden");
}

function loadConfigPage() {

  document.getElementById("problem_field").classList.add("hidden");
  document.getElementById("participants_field").classList.add("hidden");

  document.getElementById("config_field").classList.remove("hidden");
}