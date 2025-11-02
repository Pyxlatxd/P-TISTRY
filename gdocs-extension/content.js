// content.js
window.addEventListener('load', function () {
  // Wait for the Google Docs menu bar to load
  const intervalId = setInterval(function () {
    const toolbar = document.querySelector('.docs-toolbar');
    if (toolbar) {
      clearInterval(intervalId);

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
    }
  }, 1000); // Check every second until the toolbar is loaded
});
