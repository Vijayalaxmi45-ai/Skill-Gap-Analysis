document.addEventListener('DOMContentLoaded', function() {
  // Global variables
  let userSkills = [];
  let charts = {};
  let uploadedFile = null;

  // Initialize dashboard
  initializeDashboard();

  function initializeDashboard() {
    setupFileUpload();
    setupSkillInput();
    setupAnalyzeButton();
    setupChatbot();
    setupFeedback();
    loadInitialData();
  }

  // File Upload Functionality
  function setupFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('resumeUpload');
    const uploadStatus = document.getElementById('uploadStatus');

    uploadArea.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', (e) => {
      e.preventDefault();
      uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
      uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadArea.classList.remove('dragover');
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        handleFileSelect({ target: { files: files } });
      }
    });
  }

  function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
      uploadedFile = file;
      const uploadStatus = document.getElementById('uploadStatus');
      uploadStatus.innerHTML = `
        <div class="alert alert-success">
          <i class="bi bi-check-circle me-2"></i>
          File selected: ${file.name}
        </div>
      `;
    }
  }

  // Skill Input Functionality
  function setupSkillInput() {
    const skillInput = document.getElementById('skillInput');
    const addSkillBtn = document.getElementById('addSkillBtn');
    const skillTags = document.getElementById('skillTags');

    addSkillBtn.addEventListener('click', addSkill);
    skillInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        addSkill();
      }
    });

    function addSkill() {
      const skill = skillInput.value.trim();
      if (skill && !userSkills.includes(skill)) {
        userSkills.push(skill);
        updateSkillTags();
        skillInput.value = '';
      }
    }

    function updateSkillTags() {
      skillTags.innerHTML = userSkills.map(skill => `
        <span class="skill-tag">
          ${skill}
          <span class="remove" onclick="removeSkill('${skill}')">&times;</span>
        </span>
      `).join('');
    }

    window.removeSkill = function(skill) {
      userSkills = userSkills.filter(s => s !== skill);
      updateSkillTags();
    };
  }

  // Analyze Button Functionality
  function setupAnalyzeButton() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    analyzeBtn.addEventListener('click', performAnalysis);
  }

  async function performAnalysis() {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const analysisResults = document.getElementById('analysisResults');
    
    // Show loading state
    analyzeBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Analyzing...';
    analyzeBtn.disabled = true;

    try {
      const role = document.getElementById('roleSelect').value;
      const company = document.getElementById('companySelect').value;

      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          skills: userSkills,
          role: role,
          company: company,
          resume_path: uploadedFile ? uploadedFile.name : null
        })
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      displayAnalysisResults(data);
      analysisResults.style.display = 'block';
      analysisResults.scrollIntoView({ behavior: 'smooth' });

    } catch (error) {
      alert('Analysis failed. Please try again.');
      console.error('Analysis error:', error);
    } finally {
      analyzeBtn.innerHTML = '<i class="bi bi-graph-up me-2"></i>Analyze My Gap';
      analyzeBtn.disabled = false;
    }
  }

  function displayAnalysisResults(data) {
    // Update summary cards
    document.getElementById('careerFitScore').textContent = data.careerFitScore + '%';
    document.getElementById('matchedSkills').textContent = data.matchedSkills.length;
    document.getElementById('missingSkills').textContent = data.missingSkills.length;
    document.getElementById('recommendedJobs').textContent = data.suggestedCompanies ? data.suggestedCompanies.length : 0;

    // Render charts
    renderCharts(data);

    // Update job matches
    updateJobMatches(data);

    // Update learning recommendations
    updateLearningRecommendations(data);

    // Update market insights
    updateMarketInsights(data);
  }

  function renderCharts(data) {
    // Skill Match Pie Chart
    const pieCtx = document.getElementById('skillPieChart').getContext('2d');
    if (charts.skillPie) charts.skillPie.destroy();
    charts.skillPie = new Chart(pieCtx, {
      type: 'pie',
      data: {
        labels: ['Matched Skills', 'Missing Skills'],
        datasets: [{
          data: [data.matchedSkills.length, data.missingSkills.length],
          backgroundColor: ['#28a745', '#dc3545'],
          borderWidth: 2,
          borderColor: '#fff'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom'
          }
        }
      }
    });

    // Missing Skills Bar Chart
    const barCtx = document.getElementById('missingSkillsChart').getContext('2d');
    if (charts.missingSkills) charts.missingSkills.destroy();
    charts.missingSkills = new Chart(barCtx, {
      type: 'bar',
      data: {
        labels: data.missingSkills.slice(0, 5),
        datasets: [{
          label: 'Importance Level',
          data: data.prioritySkills ? data.prioritySkills.slice(0, 5).map(s => s.importance) : [5, 4, 3, 2, 1],
          backgroundColor: '#ffc107',
          borderColor: '#ff8c00',
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 10
          }
        }
      }
    });

    // Radar Chart for Skill Profile
    const radarCtx = document.getElementById('radarChart').getContext('2d');
    if (charts.radar) charts.radar.destroy();
    charts.radar = new Chart(radarCtx, {
      type: 'radar',
      data: {
        labels: ['Technical Skills', 'Soft Skills', 'Industry Knowledge', 'Tools & Software', 'Certifications'],
        datasets: [{
          label: 'Your Profile',
          data: [7, 6, 5, 8, 4],
          backgroundColor: 'rgba(0, 123, 255, 0.2)',
          borderColor: '#007bff',
          borderWidth: 2
        }, {
          label: 'Target Role',
          data: [9, 7, 8, 9, 6],
          backgroundColor: 'rgba(40, 167, 69, 0.2)',
          borderColor: '#28a745',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            beginAtZero: true,
            max: 10
          }
        }
      }
    });

    // Progress Line Chart
    const lineCtx = document.getElementById('progressChart').getContext('2d');
    if (charts.progress) charts.progress.destroy();
    charts.progress = new Chart(lineCtx, {
      type: 'line',
      data: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        datasets: [{
          label: 'Skill Growth %',
          data: [20, 35, 45, 60, 70, data.careerFitScore],
          borderColor: '#007bff',
          backgroundColor: 'rgba(0, 123, 255, 0.1)',
          borderWidth: 3,
          fill: true,
          tension: 0.4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            max: 100
          }
        }
      }
    });
  }

  function updateJobMatches(data) {
    const jobMatchesList = document.getElementById('jobMatchesList');
    const mockJobs = [
      { company: 'TechCorp', role: 'Data Analyst', match: 85, salary: '$65,000 - $85,000' },
      { company: 'DataFlow', role: 'Business Analyst', match: 78, salary: '$60,000 - $80,000' },
      { company: 'Analytics Inc', role: 'Data Scientist', match: 72, salary: '$75,000 - $95,000' }
    ];

    jobMatchesList.innerHTML = mockJobs.map(job => `
      <div class="job-match-item">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <h6 class="mb-1">${job.role} at ${job.company}</h6>
            <small class="text-muted">${job.salary}</small>
          </div>
          <div class="d-flex align-items-center gap-2">
            <span class="match-percentage">${job.match}% Match</span>
            <button class="btn btn-sm btn-primary">Apply Now</button>
          </div>
        </div>
      </div>
    `).join('');
  }

  function updateLearningRecommendations(data) {
    const skillProgressLadder = document.getElementById('skillProgressLadder');
    const recommendedCourses = document.getElementById('recommendedCourses');

    // Skill Progress Ladder
    const skills = ['Python', 'SQL', 'Machine Learning', 'Data Visualization'];
    skillProgressLadder.innerHTML = skills.map(skill => `
      <div class="skill-progress">
        <div class="d-flex justify-content-between mb-2">
          <span>${skill}</span>
          <span>75%</span>
        </div>
        <div class="progress-bar-custom">
          <div class="progress-fill" style="width: 75%"></div>
        </div>
      </div>
    `).join('');

    // Recommended Courses
    const courses = [
      { name: 'Python for Data Science', platform: 'Coursera', duration: '4 weeks', link: '#' },
      { name: 'SQL Fundamentals', platform: 'Udemy', duration: '2 weeks', link: '#' },
      { name: 'Machine Learning Basics', platform: 'NPTEL', duration: '6 weeks', link: '#' }
    ];

    recommendedCourses.innerHTML = courses.map(course => `
      <div class="course-recommendation">
        <h6>${course.name}</h6>
        <p class="mb-1"><strong>Platform:</strong> ${course.platform}</p>
        <p class="mb-2"><strong>Duration:</strong> ${course.duration}</p>
        <a href="${course.link}" class="btn btn-sm btn-success">Enroll Now</a>
      </div>
    `).join('');
  }

  function updateMarketInsights(data) {
    const inDemandSkills = document.getElementById('inDemandSkills');
    const salaryRange = document.getElementById('salaryRange');

    const skills = ['Python', 'SQL', 'Machine Learning', 'Data Visualization', 'Statistics'];
    inDemandSkills.innerHTML = skills.map(skill => `
      <li class="d-flex justify-content-between">
        <span>${skill}</span>
        <span class="badge bg-primary">High</span>
      </li>
    `).join('');

    salaryRange.textContent = '$50,000 - $80,000';
  }

  // Chatbot Functionality
  function setupChatbot() {
    const chatbotBtn = document.getElementById('chatbotBtn');
    chatbotBtn.addEventListener('click', toggleChatbot);
  }

  function toggleChatbot() {
    // Simple chatbot implementation
    const message = prompt('Ask me anything about your career or skills:');
    if (message) {
      alert('AI Assistant: Based on your question, I recommend focusing on Python and SQL skills. These are highly in-demand in the current job market.');
    }
  }

  // Feedback Functionality
  function setupFeedback() {
    const downloadBtn = document.getElementById('downloadReport');
    const shareBtn = document.getElementById('shareInsights');

    downloadBtn.addEventListener('click', downloadReport);
    shareBtn.addEventListener('click', shareInsights);
  }

  function downloadReport() {
    // Generate and download report
    const reportContent = `
      AI Career Campus - Skill Gap Analysis Report
      ===========================================
      
      Career Fit Score: ${document.getElementById('careerFitScore').textContent}
      Matched Skills: ${document.getElementById('matchedSkills').textContent}
      Missing Skills: ${document.getElementById('missingSkills').textContent}
      
      Recommendations:
      - Focus on Python and SQL skills
      - Consider machine learning courses
      - Build data visualization portfolio
      
      Generated on: ${new Date().toLocaleDateString()}
    `;

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'skill-gap-analysis-report.txt';
    a.click();
    window.URL.revokeObjectURL(url);
  }

  function shareInsights() {
    if (navigator.share) {
      navigator.share({
        title: 'My Skill Gap Analysis',
        text: 'Check out my career analysis from AI Career Campus!',
        url: window.location.href
      });
    } else {
      // Fallback for browsers that don't support Web Share API
      const url = window.location.href;
      navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard!');
      });
    }
  }

  // Load initial data if available
  function loadInitialData() {
  const initialScript = document.getElementById('initialChartData');
    if (initialScript) {
      try {
        const initialData = JSON.parse(initialScript.textContent || '{}');
        if (initialData && Object.keys(initialData).length > 0) {
          displayAnalysisResults(initialData);
          document.getElementById('analysisResults').style.display = 'block';
        }
      } catch (e) {
        console.warn('Invalid initial chart data', e);
      }
    }
  }

  // Expose functions globally for backward compatibility
  window.renderChartsFromData = function(data) {
    displayAnalysisResults(data);
  };
});