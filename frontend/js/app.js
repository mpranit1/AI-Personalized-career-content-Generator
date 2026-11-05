// App State
let currentProfile = JSON.parse(JSON.stringify(PRESET_PROFILES["cs_ml_junior"]));
let currentDossier = null;
let radarChartInstance = null;
let categoryChartInstance = null;

// Initialize on DOM ready
document.addEventListener("DOMContentLoaded", () => {
    populateFormFromState(currentProfile);
    setupEventListeners();
    generateCareerDossier(); // Auto-generate initial preview
});

function setupEventListeners() {
    // Preset dropdown
    const presetSelect = document.getElementById("presetSelector");
    presetSelect.addEventListener("change", (e) => {
        const key = e.target.value;
        if (PRESET_PROFILES[key]) {
            currentProfile = JSON.parse(JSON.stringify(PRESET_PROFILES[key]));
            populateFormFromState(currentProfile);
            showToast(`Loaded preset for ${currentProfile.name}`);
            generateCareerDossier();
        }
    });

    // Form submission
    const profileForm = document.getElementById("profileForm");
    profileForm.addEventListener("submit", (e) => {
        e.preventDefault();
        readFormIntoState();
        generateCareerDossier();
    });

    // Add skill button
    document.getElementById("addSkillBtn").addEventListener("click", () => {
        const nameInput = document.getElementById("newSkillName");
        const profSelect = document.getElementById("newSkillProf");
        const name = nameInput.value.trim();
        if (name) {
            currentProfile.skills.push({
                name: name,
                proficiency: profSelect.value,
                category: "Programming & Languages",
                years_experience: 1.0
            });
            nameInput.value = "";
            renderSkillsList();
        }
    });

    // Add project button
    document.getElementById("addProjectBtn").addEventListener("click", () => {
        currentProfile.projects.push({
            title: "New Technical Project",
            description: "Describe the core challenge, architecture, and results achieved.",
            role: "Developer",
            tech_stack: ["Python", "FastAPI"],
            highlights: ["Achieved measurable benchmark improvement"],
            link: ""
        });
        renderProjectsList();
    });

    // Tab buttons
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab-btn").forEach(b => {
                b.classList.remove("border-indigo-600", "text-indigo-600", "font-semibold");
                b.classList.add("border-transparent", "text-slate-500");
            });
            btn.classList.add("border-indigo-600", "text-indigo-600", "font-semibold");
            btn.classList.remove("border-transparent", "text-slate-500");

            const tabId = btn.getAttribute("data-tab");
            document.querySelectorAll(".tab-content").forEach(panel => {
                panel.classList.add("hidden");
            });
            const activePanel = document.getElementById(tabId);
            if (activePanel) activePanel.classList.remove("hidden");
        });
    });

    // Export buttons
    document.getElementById("printDossierBtn").addEventListener("click", () => {
        if (!currentDossier) return;
        const printWindow = window.open("", "_blank");
        printWindow.document.write(currentDossier.formatted_artifacts.career_dossier_html);
        printWindow.document.close();
        printWindow.focus();
        setTimeout(() => printWindow.print(), 500);
    });

    document.getElementById("downloadJsonBtn").addEventListener("click", () => {
        if (!currentDossier) return;
        const blob = new Blob([JSON.stringify(currentDossier, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${currentProfile.name.replace(/\s+/g, '_')}_Career_Dossier.json`;
        a.click();
        URL.revokeObjectURL(url);
    });

    // Copy actions
    setupCopyAction("copyResumeBtn", () => currentDossier?.formatted_artifacts?.markdown_resume);
    setupCopyAction("copyLinkedinBtn", () => currentDossier?.formatted_artifacts?.linkedin_profile_text);
    setupCopyAction("copyExecSummaryBtn", () => currentDossier?.professional_summary?.executive_summary);
    setupCopyAction("copyPitchBtn", () => currentDossier?.professional_summary?.elevator_pitch_30s);
}

function setupCopyAction(btnId, getContentFn) {
    const btn = document.getElementById(btnId);
    if (!btn) return;
    btn.addEventListener("click", async () => {
        const text = getContentFn();
        if (text) {
            await navigator.clipboard.writeText(text);
            showToast("Copied to clipboard!");
        }
    });
}

function populateFormFromState(p) {
    document.getElementById("studentName").value = p.name || "";
    document.getElementById("studentEmail").value = p.email || "";
    document.getElementById("studentInstitution").value = p.education.institution || "";
    document.getElementById("studentDegree").value = p.education.degree || "";
    document.getElementById("studentMajor").value = p.education.major || "";
    document.getElementById("studentGradYear").value = p.education.graduation_year || 2026;
    document.getElementById("studentGpa").value = p.education.gpa || "";
    document.getElementById("studentCoursework").value = (p.education.coursework || []).join(", ");
    document.getElementById("targetRole").value = p.career_goal.target_role || "";
    document.getElementById("targetSeniority").value = p.career_goal.seniority_level || "";
    document.getElementById("weeklyHours").value = p.hours_per_week_available || 10;
    document.getElementById("academicInterests").value = (p.academic_interests || []).join(", ");

    renderSkillsList();
    renderProjectsList();
}

function readFormIntoState() {
    currentProfile.name = document.getElementById("studentName").value.trim();
    currentProfile.email = document.getElementById("studentEmail").value.trim();
    currentProfile.education.institution = document.getElementById("studentInstitution").value.trim();
    currentProfile.education.degree = document.getElementById("studentDegree").value.trim();
    currentProfile.education.major = document.getElementById("studentMajor").value.trim();
    currentProfile.education.graduation_year = parseInt(document.getElementById("studentGradYear").value, 10) || 2026;
    currentProfile.education.gpa = document.getElementById("studentGpa").value.trim();
    currentProfile.education.coursework = document.getElementById("studentCoursework").value
        .split(",")
        .map(s => s.trim())
        .filter(Boolean);
    currentProfile.career_goal.target_role = document.getElementById("targetRole").value.trim();
    currentProfile.career_goal.seniority_level = document.getElementById("targetSeniority").value.trim();
    currentProfile.hours_per_week_available = parseInt(document.getElementById("weeklyHours").value, 10) || 10;
    currentProfile.academic_interests = document.getElementById("academicInterests").value
        .split(",")
        .map(s => s.trim())
        .filter(Boolean);
}

function renderSkillsList() {
    const container = document.getElementById("skillsListContainer");
    container.innerHTML = "";

    currentProfile.skills.forEach((skill, idx) => {
        const badge = document.createElement("div");
        badge.className = "flex items-center gap-1.5 bg-slate-100 border border-slate-300 rounded-lg px-2.5 py-1 text-xs text-slate-800";
        badge.innerHTML = `
            <span class="font-medium">${skill.name}</span>
            <select class="bg-transparent border-0 text-[11px] font-semibold text-indigo-700 cursor-pointer focus:outline-none" onchange="updateSkillProf(${idx}, this.value)">
                <option value="beginner" ${skill.proficiency === "beginner" ? "selected" : ""}>Beginner</option>
                <option value="intermediate" ${skill.proficiency === "intermediate" ? "selected" : ""}>Interm</option>
                <option value="advanced" ${skill.proficiency === "advanced" ? "selected" : ""}>Advanced</option>
                <option value="expert" ${skill.proficiency === "expert" ? "selected" : ""}>Expert</option>
            </select>
            <button type="button" class="text-slate-400 hover:text-red-500 ml-1" onclick="removeSkill(${idx})">&times;</button>
        `;
        container.appendChild(badge);
    });
}

window.updateSkillProf = function(idx, val) {
    if (currentProfile.skills[idx]) {
        currentProfile.skills[idx].proficiency = val;
    }
};

window.removeSkill = function(idx) {
    currentProfile.skills.splice(idx, 1);
    renderSkillsList();
};

function renderProjectsList() {
    const container = document.getElementById("projectsListContainer");
    container.innerHTML = "";

    currentProfile.projects.forEach((proj, idx) => {
        const card = document.createElement("div");
        card.className = "p-3 bg-slate-50 border border-slate-200 rounded-lg text-xs space-y-1.5 relative";
        card.innerHTML = `
            <button type="button" class="absolute top-2 right-2 text-slate-400 hover:text-red-500" onclick="removeProject(${idx})">&times;</button>
            <div class="font-semibold text-slate-900">${proj.title}</div>
            <div class="text-slate-600 line-clamp-2">${proj.description}</div>
            <div class="flex flex-wrap gap-1 text-[11px] text-slate-500">
                ${(proj.tech_stack || []).map(t => `<span class="bg-white border px-1.5 py-0.5 rounded">${t}</span>`).join("")}
            </div>
        `;
        container.appendChild(card);
    });
}

window.removeProject = function(idx) {
    currentProfile.projects.splice(idx, 1);
    renderProjectsList();
};

async function generateCareerDossier() {
    const loadingOverlay = document.getElementById("loadingOverlay");
    loadingOverlay.classList.remove("hidden");

    try {
        const response = await fetch("/api/v1/generate", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(currentProfile)
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || "Generation failed");
        }

        currentDossier = await response.json();
        renderDossierView(currentDossier);
        showToast("Career dossier generated successfully!");
    } catch (err) {
        console.error(err);
        showToast(`Error: ${err.message}`, "error");
    } finally {
        loadingOverlay.classList.add("hidden");
    }
}

function renderDossierView(dossier) {
    const p = dossier.student_profile;
    const summary = dossier.professional_summary;
    const gap = dossier.skill_gap_report;
    const roadmap = dossier.learning_roadmap;
    const prep = dossier.interview_prep;
    const audit = dossier.consistency_audit;
    const formatted = dossier.formatted_artifacts;

    // Header badge
    document.getElementById("engineBadge").textContent = dossier.model_used;

    // ==========================================
    // Tab 1: Executive Overview & Professional Summary
    // ==========================================
    document.getElementById("overviewName").textContent = p.name;
    document.getElementById("overviewTargetRole").textContent = summary.target_role;
    document.getElementById("overviewDegree").textContent = `${p.education.degree} in ${p.education.major} • ${p.education.institution} (${p.education.graduation_year})`;
    document.getElementById("overviewReadinessBadge").textContent = gap.readiness_tier;
    document.getElementById("readinessScoreVal").textContent = `${gap.overall_readiness_score}%`;
    document.getElementById("consistencyScoreVal").textContent = `${audit.overall_consistency_score}%`;

    document.getElementById("execSummaryText").textContent = summary.executive_summary;
    document.getElementById("linkedinAboutText").textContent = summary.linkedin_about;
    document.getElementById("elevatorPitchText").textContent = `"${summary.elevator_pitch_30s}"`;

    // Value propositions
    const valPropsContainer = document.getElementById("valPropsContainer");
    valPropsContainer.innerHTML = summary.key_value_propositions.map(prop => `
        <div class="flex items-start gap-2.5 p-3 bg-indigo-50/50 border border-indigo-100 rounded-lg text-sm text-slate-800">
            <span class="text-indigo-600 font-bold mt-0.5">&bull;</span>
            <div>${prop}</div>
        </div>
    `).join("");

    // Core competencies chips
    const coreCompContainer = document.getElementById("coreCompContainer");
    coreCompContainer.innerHTML = summary.core_competencies.map(comp => `
        <span class="px-2.5 py-1 bg-slate-100 border border-slate-200 rounded-md text-xs font-medium text-slate-700">${comp}</span>
    `).join("");

    // Render Radar Chart for Category Breakdown
    renderRadarChart(gap.category_scores);

    // ==========================================
    // Tab 2: Skill-Gap Analyzer & Benchmark Matrix
    // ==========================================
    document.getElementById("statMatchedCount").textContent = gap.matched_skills_count;
    document.getElementById("statPartialCount").textContent = gap.partial_skills_count;
    document.getElementById("statMissingCount").textContent = gap.missing_skills_count;
    document.getElementById("statDiffCount").textContent = gap.differentiator_skills_count;
    document.getElementById("gapAssessmentText").textContent = gap.readiness_assessment;

    renderGapsTable(gap.gaps);

    // ==========================================
    // Tab 3: Personalized Learning Roadmap
    // ==========================================
    document.getElementById("roadmapMeta").textContent = `${roadmap.total_weeks} Weeks • ${roadmap.weekly_hours} Hours/Week • ${roadmap.total_study_hours} Total Study Hours`;
    
    const roadmapContainer = document.getElementById("roadmapPhasesContainer");
    roadmapContainer.innerHTML = roadmap.phases.map(phase => `
        <div class="border border-slate-200 rounded-xl p-5 bg-white shadow-sm space-y-4">
            <div class="flex items-center justify-between border-b pb-3">
                <div>
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-700">Phase ${phase.phase_number}</span>
                    <h3 class="text-base font-bold text-slate-900 mt-1">${phase.phase_name}</h3>
                    <p class="text-xs text-slate-500">${phase.focus_summary}</p>
                </div>
                <div class="text-right">
                    <span class="text-sm font-semibold text-slate-800">${phase.duration_weeks} Weeks</span>
                </div>
            </div>

            <div class="space-y-3">
                ${phase.recommendations.map(rec => `
                    <div class="bg-slate-50 border border-slate-200 rounded-lg p-3.5 space-y-2">
                        <div class="flex items-center justify-between">
                            <span class="font-bold text-sm text-slate-900">${rec.gap_skill}</span>
                            <span class="text-xs px-2 py-0.5 rounded font-medium bg-blue-100 text-blue-700">Target: ${rec.target_proficiency}</span>
                        </div>
                        <p class="text-xs text-slate-600">${rec.recommended_action}</p>
                        <div class="p-2.5 bg-white rounded border border-slate-200 text-xs text-slate-700 space-y-1">
                            <div><strong>Capstone Task:</strong> ${rec.capstone_mini_project}</div>
                            <div class="text-indigo-600"><strong>Deliverable:</strong> ${rec.verification_deliverable}</div>
                        </div>
                        ${rec.curated_resources && rec.curated_resources.length ? `
                            <div class="pt-1">
                                <span class="text-[11px] font-semibold text-slate-500 uppercase tracking-wide">Recommended Resources:</span>
                                <div class="flex flex-wrap gap-2 mt-1">
                                    ${rec.curated_resources.map(res => `
                                        <div class="px-2 py-1 bg-white border border-slate-200 rounded text-xs text-slate-700">
                                            📚 <strong>${res.title}</strong> (${res.resource_type} • ${res.url_or_platform} • ~${res.estimated_hours}h)
                                        </div>
                                    `).join("")}
                                </div>
                            </div>
                        ` : ''}
                    </div>
                `).join("")}
            </div>
        </div>
    `).join("");

    // Suggested certifications
    const certsContainer = document.getElementById("suggestedCertsContainer");
    certsContainer.innerHTML = (roadmap.suggested_certifications || []).map(c => `
        <span class="px-3 py-1 bg-emerald-50 border border-emerald-200 rounded-full text-xs font-semibold text-emerald-800">
            🏅 ${c}
        </span>
    `).join("");

    // ==========================================
    // Tab 4: Interview Preparation Material
    // ==========================================
    renderInterviewPrepTab(prep);

    // ==========================================
    // Tab 5: Cross-Format Consistency Audit
    // ==========================================
    renderConsistencyAuditTab(audit);

    // ==========================================
    // Tab 6: Formats & Exports
    // ==========================================
    document.getElementById("resumeMarkdownPreview").textContent = formatted.markdown_resume;
    document.getElementById("linkedinTextPreview").textContent = formatted.linkedin_profile_text;
    document.getElementById("interviewGuidePreview").textContent = formatted.interview_study_sheet_markdown;
}

function renderGapsTable(gaps) {
    const tbody = document.getElementById("gapsTableBody");
    tbody.innerHTML = gaps.map(g => {
        let badgeClass = "bg-emerald-100 text-emerald-800";
        if (g.status === "partial") badgeClass = "bg-amber-100 text-amber-800";
        if (g.status === "missing") badgeClass = "bg-rose-100 text-rose-800";
        if (g.status === "differentiator") badgeClass = "bg-blue-100 text-blue-800";

        let sevBadge = "";
        if (g.severity === "critical") sevBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-600 text-white">CRITICAL</span>';
        else if (g.severity === "high") sevBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500 text-white">HIGH</span>';
        else if (g.severity === "medium") sevBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-200 text-slate-700">MEDIUM</span>';

        return `
            <tr class="hover:bg-slate-50/75 border-b border-slate-100 text-xs">
                <td class="py-3 px-4 font-semibold text-slate-900">${g.skill_name}</td>
                <td class="py-3 px-4 text-slate-600">${g.category}</td>
                <td class="py-3 px-4">
                    <span class="px-2 py-0.5 rounded-full text-[11px] font-semibold ${badgeClass}">
                        ${g.status.toUpperCase()}
                    </span>
                </td>
                <td class="py-3 px-4 capitalize text-slate-700">${g.current_proficiency || '—'}</td>
                <td class="py-3 px-4 capitalize font-medium text-slate-900">${g.required_proficiency}</td>
                <td class="py-3 px-4">${sevBadge}</td>
                <td class="py-3 px-4 text-slate-600 max-w-xs">${g.impact_analysis}</td>
            </tr>
        `;
    }).join("");
}

function renderInterviewPrepTab(prep) {
    // Technical questions
    const techContainer = document.getElementById("techQuestionsContainer");
    techContainer.innerHTML = prep.technical_questions.map((q, idx) => `
        <div class="border border-slate-200 rounded-lg p-4 bg-white space-y-2">
            <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-indigo-600 uppercase tracking-wide">${q.topic}</span>
                <span class="text-xs text-slate-400">Technical Round</span>
            </div>
            <div class="text-sm font-semibold text-slate-900">${q.question}</div>
            <div class="p-3 bg-slate-50 border border-slate-200 rounded text-xs text-slate-800 space-y-1.5">
                <div class="font-semibold text-slate-900">Model Answer:</div>
                <p class="leading-relaxed text-slate-700">${q.sample_ideal_answer}</p>
                <div class="pt-1 text-slate-500">
                    <strong>Key Concepts:</strong> ${q.key_concepts_to_demonstrate.join(", ")}
                </div>
                <div class="text-rose-600">
                    <strong>Pitfall to Avoid:</strong> ${q.pitfalls_to_avoid.join("; ")}
                </div>
            </div>
        </div>
    `).join("");

    // Behavioral questions (STAR)
    const behContainer = document.getElementById("behQuestionsContainer");
    behContainer.innerHTML = prep.behavioral_questions.map((q, idx) => `
        <div class="border border-slate-200 rounded-lg p-4 bg-white space-y-2">
            <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-amber-600 uppercase tracking-wide">${q.topic}</span>
                <span class="text-xs text-slate-400">Behavioral / STAR</span>
            </div>
            <div class="text-sm font-semibold text-slate-900">${q.question}</div>
            ${q.star_breakdown ? `
                <div class="grid grid-cols-2 gap-2 text-xs bg-amber-50/40 border border-amber-100 p-3 rounded">
                    <div><strong>Situation:</strong> ${q.star_breakdown.situation}</div>
                    <div><strong>Task:</strong> ${q.star_breakdown.task}</div>
                    <div><strong>Action:</strong> ${q.star_breakdown.action}</div>
                    <div><strong>Result:</strong> ${q.star_breakdown.result}</div>
                </div>
            ` : `
                <div class="p-3 bg-slate-50 rounded text-xs text-slate-700">${q.sample_ideal_answer}</div>
            `}
        </div>
    `).join("");

    // Project defense questions
    const projContainer = document.getElementById("projectDefenseContainer");
    projContainer.innerHTML = prep.project_defense_questions.map((q, idx) => `
        <div class="border border-slate-200 rounded-lg p-4 bg-white space-y-2">
            <div class="flex items-center justify-between">
                <span class="text-xs font-bold text-sky-600 uppercase tracking-wide">${q.topic}</span>
                <span class="text-xs text-slate-400">Project Defense</span>
            </div>
            <div class="text-sm font-semibold text-slate-900">${q.question}</div>
            <div class="p-3 bg-slate-50 border border-slate-200 rounded text-xs text-slate-800">
                <strong>Expected Technical Defense:</strong>
                <p class="mt-1 text-slate-700">${q.sample_ideal_answer}</p>
            </div>
        </div>
    `).join("");

    // Cheat sheet
    document.getElementById("cheatSheetList").innerHTML = prep.day_before_cheat_sheet.map(item => `
        <li class="flex items-start gap-2 text-xs text-slate-700">
            <span class="text-emerald-500 font-bold">✓</span>
            <span>${item}</span>
        </li>
    `).join("");

    // Red flags
    document.getElementById("redFlagsList").innerHTML = prep.interviewer_red_flags.map(item => `
        <li class="flex items-start gap-2 text-xs text-slate-700">
            <span class="text-rose-500 font-bold">⚠️</span>
            <span>${item}</span>
        </li>
    `).join("");
}

function renderConsistencyAuditTab(audit) {
    document.getElementById("auditOverallScore").textContent = `${audit.overall_consistency_score}%`;
    const statusPill = document.getElementById("auditStatusPill");
    if (audit.is_consistent) {
        statusPill.className = "px-3 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800";
        statusPill.textContent = "COHERENCE VERIFIED (PASS)";
    } else {
        statusPill.className = "px-3 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800";
        statusPill.textContent = "ALIGNMENT ACTION NEEDED";
    }

    // Dimension cards
    const dimContainer = document.getElementById("auditDimensionsContainer");
    dimContainer.innerHTML = Object.entries(audit.dimension_scores).map(([dim, score]) => `
        <div class="p-3 bg-white border border-slate-200 rounded-lg text-center">
            <div class="text-xs text-slate-500 capitalize">${dim.replace(/_/g, ' ')}</div>
            <div class="text-lg font-bold text-slate-900 mt-1">${score}%</div>
        </div>
    `).join("");

    // Checks list
    const checksContainer = document.getElementById("auditChecksContainer");
    checksContainer.innerHTML = audit.audit_checks.map(chk => {
        let badge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">PASS</span>';
        if (chk.status === "WARN") badge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">WARN</span>';
        if (chk.status === "FAIL") badge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800">FAIL</span>';

        return `
            <div class="p-4 bg-white border border-slate-200 rounded-lg space-y-1.5">
                <div class="flex items-center justify-between">
                    <span class="font-bold text-sm text-slate-900">${chk.check_name}</span>
                    ${badge}
                </div>
                <p class="text-xs text-slate-600">${chk.details}</p>
            </div>
        `;
    }).join("");

    // Reconciliation notes
    const notesContainer = document.getElementById("auditNotesContainer");
    if (audit.reconciliation_notes && audit.reconciliation_notes.length) {
        notesContainer.classList.remove("hidden");
        document.getElementById("auditNotesList").innerHTML = audit.reconciliation_notes.map(n => `
            <li class="text-xs text-slate-700">&bull; ${n}</li>
        `).join("");
    } else {
        notesContainer.classList.add("hidden");
    }
}

function renderRadarChart(categoryScores) {
    const ctx = document.getElementById("categoryRadarChart");
    if (!ctx) return;

    const labels = Object.keys(categoryScores);
    const data = Object.values(categoryScores);

    if (radarChartInstance) {
        radarChartInstance.destroy();
    }

    radarChartInstance = new Chart(ctx, {
        type: "radar",
        data: {
            labels: labels,
            datasets: [{
                label: "Readiness Index (%)",
                data: data,
                backgroundColor: "rgba(79, 70, 229, 0.2)",
                borderColor: "rgba(79, 70, 229, 1)",
                pointBackgroundColor: "rgba(79, 70, 229, 1)",
                pointBorderColor: "#fff",
                pointHoverBackgroundColor: "#fff",
                pointHoverBorderColor: "rgba(79, 70, 229, 1)"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: "#e2e8f0" },
                    grid: { color: "#e2e8f0" },
                    suggestedMin: 0,
                    suggestedMax: 100,
                    ticks: { stepSize: 20, display: false }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

function showToast(msg, type = "success") {
    const toast = document.createElement("div");
    toast.className = `fixed bottom-5 right-5 z-50 px-4 py-2.5 rounded-lg shadow-lg text-xs font-semibold text-white transition-all transform duration-300 ${
        type === "error" ? "bg-rose-600" : "bg-slate-900"
    }`;
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
    }, 2800);
}

