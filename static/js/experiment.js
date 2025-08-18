const jsPsych = initJsPsych({
    on_finish: async function() {
      // Send ALL data to backend
      const payload = jsPsych.data.get().values();
      try {
        await fetch("/save", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify(payload)
        });
      } catch(e) {
        console.error("Save failed", e);
      }
      window.location = "/done";
    }
  });
  
  const timeline = [];
  
  // A tiny example trial
  timeline.push({
    type: jsPsychHtmlButtonResponse,
    stimulus: "<p>Welcome! Ready to begin?</p>",
    choices: ["Yes"]
  });
  
  // A pretend survey question
  timeline.push({
    type: jsPsychHtmlButtonResponse,
    stimulus: "<p>How are you feeling today?</p>",
    choices: ["Great", "Okay", "Not great"]
  });
  
  jsPsych.run(timeline);
  