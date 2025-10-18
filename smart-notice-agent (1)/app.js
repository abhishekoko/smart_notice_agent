// State Management
let currentUser = null
let notices = []
let keywords = []

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  loadFromLocalStorage()
  setupEventListeners()
  checkAuthStatus()
  applyTheme()
})

// Event Listeners
function setupEventListeners() {
  // Auth Forms
  document.getElementById("loginForm").addEventListener("submit", handleLogin)
  document.getElementById("signupForm").addEventListener("submit", handleSignup)

  // Create Notice Form
  document.getElementById("createNoticeForm").addEventListener("submit", handleCreateNotice)

  // Theme Toggle
  document.getElementById("themeToggle").addEventListener("click", toggleTheme)

  // Dark Mode Toggle in Settings
  document.getElementById("darkModeToggle").addEventListener("change", (e) => {
    if (e.target.checked) {
      document.body.classList.add("dark-mode")
      localStorage.setItem("theme", "dark")
    } else {
      document.body.classList.remove("dark-mode")
      localStorage.setItem("theme", "light")
    }
  })

  // Hamburger Menu
  document.getElementById("hamburger").addEventListener("click", () => {
    document.getElementById("sidebar").classList.toggle("active")
  })

  // Search in History
  document.getElementById("searchInput").addEventListener("input", filterCompletedNotices)

  // Close modals on outside click
  document.getElementById("createModal").addEventListener("click", (e) => {
    if (e.target.id === "createModal") closeCreateModal()
  })

  document.getElementById("confirmModal").addEventListener("click", (e) => {
    if (e.target.id === "confirmModal") closeConfirmModal()
  })
}

// Authentication
function handleLogin(e) {
  e.preventDefault()
  const email = document.getElementById("loginEmail").value
  const password = document.getElementById("loginPassword").value

  if (email && password) {
    currentUser = { email, name: email.split("@")[0] }
    localStorage.setItem("currentUser", JSON.stringify(currentUser))
    showApp()
  }
}

function handleSignup(e) {
  e.preventDefault()
  const name = document.getElementById("signupName").value
  const email = document.getElementById("signupEmail").value
  const password = document.getElementById("signupPassword").value

  if (name && email && password) {
    currentUser = { name, email }
    localStorage.setItem("currentUser", JSON.stringify(currentUser))
    showApp()
  }
}

function logout() {
  currentUser = null
  localStorage.removeItem("currentUser")
  document.getElementById("mainApp").classList.remove("active")
  document.getElementById("loginPage").classList.add("active")
  document.getElementById("signupPage").classList.remove("active")
}

function checkAuthStatus() {
  const user = localStorage.getItem("currentUser")
  if (user) {
    currentUser = JSON.parse(user)
    showApp()
  }
}

function showApp() {
  document.getElementById("loginPage").classList.remove("active")
  document.getElementById("signupPage").classList.remove("active")
  document.getElementById("mainApp").classList.add("active")
  navigateTo("dashboard")
  updateDashboard()
  renderKeywords()
}

// Navigation
function navigateTo(page, e) {
  if (e) e.preventDefault()

  // Hide all pages
  document.querySelectorAll(".page").forEach((p) => p.classList.remove("active"))
  document.querySelectorAll(".nav-item").forEach((n) => n.classList.remove("active"))

  // Show selected page
  document.getElementById(page + "Page").classList.add("active")
  document.querySelector(`[data-page="${page}"]`).classList.add("active")

  // Close sidebar on mobile
  document.getElementById("sidebar").classList.remove("active")

  // Update page content
  if (page === "dashboard") {
    updateDashboard()
  } else if (page === "history") {
    updateHistory()
  } else if (page === "settings") {
    renderKeywords()
  }
}

function switchToSignup(e) {
  e.preventDefault()
  document.getElementById("loginPage").classList.remove("active")
  document.getElementById("signupPage").classList.add("active")
}

function switchToLogin(e) {
  e.preventDefault()
  document.getElementById("signupPage").classList.remove("active")
  document.getElementById("loginPage").classList.add("active")
}

// Notice Management
function handleCreateNotice(e) {
  e.preventDefault()

  const notice = {
    id: Date.now(),
    title: document.getElementById("noticeTitle").value,
    description: document.getElementById("noticeDescription").value,
    medium: document.getElementById("noticeMedium").value,
    dueDate: document.getElementById("noticeDeadline").value,
    status: "pending",
    createdDate: new Date().toISOString().split("T")[0],
  }

  notices.push(notice)
  saveToLocalStorage()
  closeCreateModal()
  updateDashboard()
  updateNotificationBadge()
}

function markNoticeComplete(id) {
  const notice = notices.find((n) => n.id === id)
  if (notice) {
    notice.status = "completed"
    notice.completedDate = new Date().toISOString().split("T")[0]
    saveToLocalStorage()
    updateDashboard()
    updateHistory()
    updateNotificationBadge()
  }
}

function deleteNotice(id) {
  showConfirmModal("Are you sure you want to delete this notice?", () => {
    notices = notices.filter((n) => n.id !== id)
    saveToLocalStorage()
    updateDashboard()
    updateHistory()
    updateNotificationBadge()
  })
}

// Dashboard
function updateDashboard() {
  const pending = notices.filter((n) => n.status === "pending")
  const completed = notices.filter((n) => n.status === "completed")

  document.getElementById("pendingCount").textContent = pending.length
  document.getElementById("completedCount").textContent = completed.length
  document.getElementById("totalCount").textContent = notices.length

  renderPendingNotices(pending)
}

function renderPendingNotices(pending) {
  const tbody = document.getElementById("pendingNoticesBody")
  tbody.innerHTML = ""

  if (pending.length === 0) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="5">No pending notices. Create one to get started!</td></tr>'
    return
  }

  pending.forEach((notice) => {
    const row = document.createElement("tr")
    row.innerHTML = `
            <td>${notice.title}</td>
            <td>${notice.description.substring(0, 50)}...</td>
            <td><span class="badge">${notice.medium}</span></td>
            <td>${notice.dueDate}</td>
            <td>
                <div class="action-buttons">
                    <button class="action-btn complete" onclick="markNoticeComplete(${notice.id})">
                        <i class="fas fa-check"></i> Done
                    </button>
                    <button class="action-btn delete" onclick="deleteNotice(${notice.id})">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                </div>
            </td>
        `
    tbody.appendChild(row)
  })
}

// History
function updateHistory() {
  const completed = notices.filter((n) => n.status === "completed")
  renderCompletedNotices(completed)
  updateAnalytics()
}

function renderCompletedNotices(completed) {
  const tbody = document.getElementById("completedNoticesBody")
  tbody.innerHTML = ""

  if (completed.length === 0) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="5">No completed notices yet.</td></tr>'
    return
  }

  completed.forEach((notice) => {
    const row = document.createElement("tr")
    row.innerHTML = `
            <td>${notice.title}</td>
            <td>${notice.description.substring(0, 50)}...</td>
            <td><span class="badge">${notice.medium}</span></td>
            <td>${notice.dueDate}</td>
            <td>${notice.completedDate || "N/A"}</td>
        `
    tbody.appendChild(row)
  })
}

function filterCompletedNotices() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase()
  const completed = notices.filter(
    (n) =>
      n.status === "completed" &&
      (n.title.toLowerCase().includes(searchTerm) || n.description.toLowerCase().includes(searchTerm)),
  )
  renderCompletedNotices(completed)
}

function updateAnalytics() {
  const completed = notices.filter((n) => n.status === "completed")
  const total = notices.length
  const completionRate = total === 0 ? 0 : Math.round((completed.length / total) * 100)

  // Calculate on-time completion
  let onTimeCount = 0
  completed.forEach((notice) => {
    if (notice.completedDate <= notice.dueDate) {
      onTimeCount++
    }
  })
  const onTimePercentage = completed.length === 0 ? 0 : Math.round((onTimeCount / completed.length) * 100)

  document.getElementById("totalCompleted").textContent = completed.length
  document.getElementById("completionRate").textContent = completionRate + "%"
  document.getElementById("onTimePercentage").textContent = onTimePercentage + "%"
}

// Keywords Management
function addKeyword() {
  const input = document.getElementById("keywordInput")
  const keyword = input.value.trim()

  if (keyword && !keywords.includes(keyword)) {
    keywords.push(keyword)
    saveToLocalStorage()
    renderKeywords()
    input.value = ""
  }
}

function removeKeyword(keyword) {
  keywords = keywords.filter((k) => k !== keyword)
  saveToLocalStorage()
  renderKeywords()
}

function renderKeywords() {
  const list = document.getElementById("keywordsList")
  list.innerHTML = ""

  keywords.forEach((keyword) => {
    const tag = document.createElement("div")
    tag.className = "keyword-tag"
    tag.innerHTML = `
            ${keyword}
            <button type="button" onclick="removeKeyword('${keyword}')">
                <i class="fas fa-times"></i>
            </button>
        `
    list.appendChild(tag)
  })
}

// Modal Management
function openCreateModal() {
  document.getElementById("createModal").classList.add("active")
}

function closeCreateModal() {
  document.getElementById("createModal").classList.remove("active")
  document.getElementById("createNoticeForm").reset()
}

function showConfirmModal(message, callback) {
  document.getElementById("confirmMessage").textContent = message
  document.getElementById("confirmBtn").onclick = () => {
    callback()
    closeConfirmModal()
  }
  document.getElementById("confirmModal").classList.add("active")
}

function closeConfirmModal() {
  document.getElementById("confirmModal").classList.remove("active")
}

// Notifications
function updateNotificationBadge() {
  const pending = notices.filter((n) => n.status === "pending").length
  document.getElementById("notificationBadge").textContent = pending
}

// Theme Management
function toggleTheme() {
  document.body.classList.toggle("dark-mode")
  const isDark = document.body.classList.contains("dark-mode")
  localStorage.setItem("theme", isDark ? "dark" : "light")
  updateThemeToggleIcon()
}

function applyTheme() {
  const theme = localStorage.getItem("theme") || "light"
  if (theme === "dark") {
    document.body.classList.add("dark-mode")
    document.getElementById("darkModeToggle").checked = true
  }
  updateThemeToggleIcon()
}

function updateThemeToggleIcon() {
  const icon = document.querySelector(".theme-toggle i")
  if (document.body.classList.contains("dark-mode")) {
    icon.classList.remove("fa-moon")
    icon.classList.add("fa-sun")
  } else {
    icon.classList.remove("fa-sun")
    icon.classList.add("fa-moon")
  }
}

// Local Storage
function saveToLocalStorage() {
  localStorage.setItem("notices", JSON.stringify(notices))
  localStorage.setItem("keywords", JSON.stringify(keywords))
}

function loadFromLocalStorage() {
  const savedNotices = localStorage.getItem("notices")
  const savedKeywords = localStorage.getItem("keywords")

  if (savedNotices) notices = JSON.parse(savedNotices)
  if (savedKeywords) keywords = JSON.parse(savedKeywords)

  // Add sample data if empty
  if (notices.length === 0) {
    notices = [
      {
        id: 1,
        title: "Submit project report",
        description: "Complete and submit the Q4 project report to management",
        medium: "Email",
        dueDate: "2025-10-20",
        status: "pending",
        createdDate: "2025-10-17",
      },
      {
        id: 2,
        title: "Team meeting reminder",
        description: "Attend the weekly team sync meeting on Zoom",
        medium: "WhatsApp",
        dueDate: "2025-10-18",
        status: "pending",
        createdDate: "2025-10-17",
      },
      {
        id: 3,
        title: "Client presentation",
        description: "Prepare and deliver presentation to client",
        medium: "Email",
        dueDate: "2025-10-19",
        status: "completed",
        createdDate: "2025-10-16",
        completedDate: "2025-10-18",
      },
    ]
    saveToLocalStorage()
  }
}
