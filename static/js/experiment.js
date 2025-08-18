const jsPsych = initJsPsych({
  on_finish: function() {
    alert("Survey finished!");
  }
});

const timeline = [{
  type: jsPsychHtmlButtonResponse,
  stimulus: "<p>Welcome! Click to start.</p>",
  choices: ["Start"]
}];

jsPsych.run(timeline);