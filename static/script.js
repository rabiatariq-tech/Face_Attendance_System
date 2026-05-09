async function fetchStudentInfo() {

    const response = await fetch('/student_info');

    const data = await response.json();

    document.getElementById('student-name')
        .innerText = data.name;

    document.getElementById('student-roll')
        .innerText = data.roll;

    document.getElementById('student-status')
        .innerText = data.status;
}

setInterval(fetchStudentInfo, 1000);