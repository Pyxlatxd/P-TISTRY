// popup.js
document.getElementById('injectButton').addEventListener('click', function() {
  chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
    chrome.scripting.executeScript({
      target: { tabId: tabs[0].id },
      func: injectButton
    });
  });
});

// Function to be injected into the page
function injectButton() {
  const toolbar = document.querySelector('.docs-toolbar');
  if (toolbar) {
    // Create your custom button
    const button = document.createElement('button');
    button.innerText = 'My Extension';
    button.style.marginLeft = '10px';
    button.style.padding = '5px';
    button.style.cursor = 'pointer';

    // Add the button to the toolbar
    toolbar.appendChild(button);

    // Add functionality to the button
    button.addEventListener('click', function () {
      alert('Button clicked!');
      // You can add additional functionality here
    });
  } else {
    console.error("Toolbar not found.");
  }
}
