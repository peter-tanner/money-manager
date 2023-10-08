const createNotification = (title, body) => {
  // Check if the browser supports the Web Notifications API
  if ("Notification" in window) {
    // Request permission to show notifications
    Notification.requestPermission().then(function (permission) {
      if (permission === "granted") {
        // Create a notification
        var notification = new Notification(title, {
          body: body,
          // url: TODO: WHEN CLICKING, GO TO EDIT PAGE FOR THAT TASK http://localhost:8000/admin/expenses/todo/1/change/
        });

        // You can add event listeners to handle user interactions with the notification
        notification.onclick = function () {
          console.log("Notification clicked");
          // Add your code to handle the click event here
        };

        notification.onclose = function () {
          console.log("Notification closed");
          // Add your code to handle the notification close event here
        };
      } else {
        console.alert("Notification permission denied");
      }
    });
  } else {
    console.alert("Web Notifications API not supported in this browser");
  }
};

function parseDateString(dateString) {
  // Remove "p.m." and split the date string
  const parts = dateString.replace("p.m.", "").split(/[\s,]+/);

  // Map month abbreviation to month number
  const months = {
    "Jan.": 0,
    "Feb.": 1,
    "Mar.": 2,
    "Apr.": 3,
    "May.": 4,
    "Jun.": 5,
    "Jul.": 6,
    "Aug.": 7,
    "Sep.": 8,
    "Oct.": 9,
    "Nov.": 10,
    "Dec.": 11,
  };

  // Extract date components
  const month = months[parts[0]];
  const day = parseInt(parts[1], 10);
  const year = parseInt(parts[2], 10);
  const hour = parseInt(parts[3].split(":")[0], 10);
  const minute = parseInt(parts[3].split(":")[1], 10);

  // Create the Date object
  const dateObject = new Date(year, month, day, hour, minute);

  return dateObject;
}

const alerted = new Set();
const url = new URL(window.location.href);
const urlParams = new URLSearchParams(url.search);
const deletedParam = urlParams.get("deleted__exact") || false;

// DO NOT NOTIFY FOR DELETED ITEMS
if (deletedParam !== "1") {
  document.addEventListener("DOMContentLoaded", function () {
    // NOTE:
    // This is to stop me from accidentally clicking away from the TODO list and disabling notifications!
    // You can still use the top links to navigate away
    const navSidebar = document.getElementById("nav-sidebar");
    const toggleNavSidebar = document.getElementById("toggle-nav-sidebar");
    navSidebar ? navSidebar.parentNode.removeChild(navSidebar) : undefined;
    toggleNavSidebar
      ? toggleNavSidebar.parentNode.removeChild(toggleNavSidebar)
      : undefined;

    function checkDueDates() {
      const rows = document.querySelectorAll("#result_list tbody tr");
      const currentDate = new Date();

      rows.forEach(function (row) {
        const titleCell = row.querySelector("th.field-title a"); // Select the due_date cell
        const title = titleCell ? titleCell.textContent : "??";
        const dueDateCell = row.querySelector("td.field-due_date"); // Select the due_date cell
        const dueDateValue = dueDateCell.textContent.trim(); // Get the due date value

        // Check if the due date cell contains a valid date
        if (dueDateValue !== "-") {
          var dueDate = parseDateString(dueDateValue);

          // Calculate the difference in days between the due date and current date
          var timeDifference = dueDate - currentDate;
          var daysDifference = Math.floor(
            timeDifference / (1000 * 60 * 60 * 24)
          );

          // Check if the due date is in 7 days
          if (
            daysDifference <= 7 &&
            daysDifference >= 0 &&
            !alerted.has(title + dueDate)
          ) {
            alerted.add(title + dueDate);
            //   alert(
            //     `Task '${
            //       row.querySelector("th.field-title a").textContent
            //     }' is due in ${daysDifference} days.`
            //   );
            createNotification(
              `Task '${
                row.querySelector("th.field-title a").textContent
              }' is due in ${daysDifference} days.`,
              "Finish this shit already!"
            );
          }
        }
      });
    }
    const resetAlerted = () => alerted.clear();
    checkDueDates();
    // Run the checkDueDates function every 5 seconds (adjust the interval as needed)
    setInterval(checkDueDates, 30 * 1000);
    setInterval(resetAlerted, 6 * 60 * 60 * 1000);
  });
}
