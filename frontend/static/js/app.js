/**
 * CodeSense AI - Frontend Application Controller
 * Milestone 2 - Prompt Engineering (SCSE4041)
 */

document.addEventListener("DOMContentLoaded", () => {
    // Elements
    const languageSelect = document.getElementById("languageSelect");
    const promptSelect = document.getElementById("promptSelect");
    const providerSelect = document.getElementById("providerSelect");
    const exampleSelect = document.getElementById("exampleSelect");
    const codeEditor = document.getElementById("codeEditor");
    const problemDesc = document.getElementById("problemDesc");
    const analyzeBtn = document.getElementById("analyzeBtn");
    const compareBtn = document.getElementById("compareBtn");
    const clearBtn = document.getElementById("clearBtn");
    const copyCodeBtn = document.getElementById("copyCodeBtn");
    const resultsContainer = document.getElementById("resultsContainer");
    const emptyState = document.getElementById("emptyState");
    const loadingState = document.getElementById("loadingState");
    const comparisonContainer = document.getElementById("comparisonContainer");
    const exportMdBtn = document.getElementById("exportMdBtn");
    const exportPdfBtn = document.getElementById("exportPdfBtn");
    const historyList = document.getElementById("historyList");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");
    const activeProviderBadge = document.getElementById("activeProviderBadge");

    let currentAnalysis = null;

    // Load Curated Examples into Dropdown
    if (typeof CODE_EXAMPLES !== "undefined" && exampleSelect) {
        CODE_EXAMPLES.forEach(ex => {
            const opt = document.createElement("option");
            opt.value = ex.id;
            opt.textContent = `[${ex.language}] ${ex.title}`;
            exampleSelect.appendChild(opt);
        });

        exampleSelect.addEventListener("change", (e) => {
            const selected = CODE_EXAMPLES.find(ex => ex.id === e.target.value);
            if (selected) {
                codeEditor.value = selected.code;
                languageSelect.value = selected.language;
                problemDesc.value = selected.description;
                showNotification(`Loaded example: ${selected.title}`, "info");
            }
        });
    }

    // Health check & initialize system status
    fetch("/api/health")
        .then(res => res.json())
        .then(data => {
            if (activeProviderBadge) {
                activeProviderBadge.textContent = `Provider: ${data.active_provider.toUpperCase()}`;
            }
        })
        .catch(err => {
            console.error("Health check error:", err);
            if (activeProviderBadge) {
                activeProviderBadge.textContent = "Offline (Mock Engine)";
            }
        });

    // Load History
    function loadHistory() {
        fetch("/api/history")
            .then(res => res.json())
            .then(data => {
                if (!historyList) return;
                historyList.innerHTML = "";
                if (!data.history || data.history.length === 0) {
                    historyList.innerHTML = `<li class="text-xs text-slate-400 py-2">No previous reviews in this session.</li>`;
                    return;
                }
                data.history.forEach(item => {
                    const li = document.createElement("li");
                    li.className = "p-2 bg-slate-50 hover:bg-slate-100 rounded text-xs border border-slate-200 cursor-pointer transition";
                    const dateStr = new Date(item.timestamp * 1000).toLocaleTimeString();
                    li.innerHTML = `
                        <div class="flex justify-between font-semibold text-slate-700">
                            <span>${item.language} (${item.prompt_version})</span>
                            <span class="text-slate-400">${dateStr}</span>
                        </div>
                        <div class="text-slate-600 truncate mt-1">${item.overall_assessment}</div>
                        <div class="text-sky-600 font-mono mt-1 text-[11px]">${item.issue_count} issue(s) detected (${item.execution_time_ms} ms)</div>
                    `;
                    li.addEventListener("click", () => {
                        codeEditor.value = item.code_snippet;
                        languageSelect.value = item.language;
                        promptSelect.value = item.prompt_version;
                    });
                    historyList.appendChild(li);
                });
            })
            .catch(err => console.error("History fetch error:", err));
    }
    loadHistory();

    // Clear Button
    clearBtn.addEventListener("click", () => {
        codeEditor.value = "";
        problemDesc.value = "";
        exampleSelect.value = "";
        resultsContainer.classList.add("hidden");
        comparisonContainer.classList.add("hidden");
        emptyState.classList.remove("hidden");
        showNotification("Code editor cleared.", "info");
    });

    // Copy Code Button
    copyCodeBtn.addEventListener("click", () => {
        if (!codeEditor.value.trim()) {
            showNotification("No code to copy!", "warning");
            return;
        }
        navigator.clipboard.writeText(codeEditor.value).then(() => {
            showNotification("Code copied to clipboard!", "success");
        });
    });

    // Clear History Button
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener("click", () => {
            fetch("/api/history", { method: "DELETE" })
                .then(() => {
                    loadHistory();
                    showNotification("History cleared.", "info");
                });
        });
    }

    // Analyze Code Action
    analyzeBtn.addEventListener("click", async () => {
        const code = codeEditor.value.trim();
        if (!code) {
            showNotification("Please enter or select code to analyze.", "warning");
            return;
        }

        // UI States
        emptyState.classList.add("hidden");
        resultsContainer.classList.add("hidden");
        comparisonContainer.classList.add("hidden");
        loadingState.classList.remove("hidden");
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = `<span class="animate-spin inline-block mr-2">🔄</span> Analyzing Code...`;

        try {
            const payload = {
                code: code,
                language: languageSelect.value,
                problem_description: problemDesc.value.trim() || null,
                prompt_version: promptSelect.value,
                provider: providerSelect.value === "auto" ? null : providerSelect.value
            };

            const response = await fetch("/api/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Analysis request failed.");
            }

            const data = await response.json();
            currentAnalysis = data;
            renderResults(data);
            loadHistory();
            showNotification("Code analysis completed successfully!", "success");
        } catch (error) {
            console.error("Analysis Error:", error);
            showNotification(`Error: ${error.message}`, "error");
            emptyState.classList.remove("hidden");
        } finally {
            loadingState.classList.add("hidden");
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = `<span>⚡</span> Analyze Code`;
        }
    });

    // Compare Prompts Action (P1 vs P2 vs P3)
    compareBtn.addEventListener("click", async () => {
        const code = codeEditor.value.trim();
        if (!code) {
            showNotification("Please enter or select code to compare prompts.", "warning");
            return;
        }

        emptyState.classList.add("hidden");
        resultsContainer.classList.add("hidden");
        comparisonContainer.classList.add("hidden");
        loadingState.classList.remove("hidden");
        compareBtn.disabled = true;
        compareBtn.innerHTML = `<span class="animate-spin inline-block mr-2">🔄</span> Evaluating P1, P2, P3...`;

        try {
            const payload = {
                code: code,
                language: languageSelect.value,
                problem_description: problemDesc.value.trim() || null
            };

            const response = await fetch("/api/compare", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Comparison request failed.");
            }

            const data = await response.json();
            renderComparison(data);
            showNotification("Prompt comparison complete! Scroll down to inspect P1 vs P2 vs P3.", "success");
        } catch (error) {
            console.error("Comparison Error:", error);
            showNotification(`Error: ${error.message}`, "error");
            emptyState.classList.remove("hidden");
        } finally {
            loadingState.classList.add("hidden");
            compareBtn.disabled = false;
            compareBtn.innerHTML = `<span>⚖️</span> Compare P1 / P2 / P3`;
        }
    });

    // Render Single Analysis Result
    function renderResults(data) {
        resultsContainer.classList.remove("hidden");

        // Metadata badges
        document.getElementById("resPromptVersion").textContent = data.prompt_version_used;
        document.getElementById("resProvider").textContent = data.provider_used;
        document.getElementById("resExecTime").textContent = `${data.execution_time_ms} ms`;
        
        // Anti-leakage badge
        const leakageBadge = document.getElementById("resLeakageBadge");
        if (data.prompt_version_used === "P1") {
            leakageBadge.className = "px-2 py-0.5 rounded text-xs font-semibold bg-rose-100 text-rose-700 border border-rose-300";
            leakageBadge.textContent = "⚠️ Potential Solution Leakage (P1 Baseline)";
        } else {
            leakageBadge.className = "px-2 py-0.5 rounded text-xs font-semibold bg-emerald-100 text-emerald-700 border border-emerald-300";
            leakageBadge.textContent = "🛡️ 0% Solution Leakage (Pedagogical Guardrail)";
        }

        // Overall Assessment
        document.getElementById("overallAssessmentText").textContent = data.overall_assessment;

        // Issues List
        const issuesContainer = document.getElementById("detectedIssuesList");
        issuesContainer.innerHTML = "";

        if (!data.issues || data.issues.length === 0) {
            issuesContainer.innerHTML = `
                <div class="p-4 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-800 flex items-center space-x-3">
                    <span class="text-2xl">🎉</span>
                    <div>
                        <h4 class="font-bold">No issues detected!</h4>
                        <p class="text-sm">The code appears syntactically sound and satisfies the required logical structure.</p>
                    </div>
                </div>
            `;
        } else {
            data.issues.forEach((issue, idx) => {
                const card = document.createElement("div");
                card.className = "bg-white border border-slate-200 rounded-lg p-4 shadow-sm space-y-3";

                const sevClass = getSeverityBadgeClass(issue.severity);

                card.innerHTML = `
                    <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2">
                        <div class="flex items-center space-x-2">
                            <span class="text-slate-400 font-mono text-xs">#${idx + 1}</span>
                            <h4 class="font-bold text-slate-800 text-base">${escapeHtml(issue.issue)}</h4>
                        </div>
                        <div class="flex items-center space-x-2">
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider ${sevClass}">
                                ${escapeHtml(issue.severity)}
                            </span>
                            <span class="text-xs bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-mono">
                                📚 ${escapeHtml(issue.concept_to_revise)}
                            </span>
                        </div>
                    </div>
                    <div>
                        <p class="text-sm text-slate-700 leading-relaxed">${escapeHtml(issue.explanation)}</p>
                    </div>
                    <div class="hint-card p-3 rounded-lg border">
                        <div class="flex items-center space-x-1.5 text-xs font-bold text-sky-800 mb-1">
                            <span>💡</span>
                            <span>SOCRATIC LEARNING HINT (Think It Through):</span>
                        </div>
                        <p class="text-xs text-sky-950 font-medium leading-relaxed">${escapeHtml(issue.hint)}</p>
                    </div>
                `;
                issuesContainer.appendChild(card);
            });
        }

        // Positive Feedback
        document.getElementById("positiveFeedbackText").textContent = data.positive_feedback;

        // Next Step
        document.getElementById("nextStepText").textContent = data.next_step;

        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // Render Side-by-Side Prompt Comparison
    function renderComparison(data) {
        comparisonContainer.classList.remove("hidden");
        const comparisonGrid = document.getElementById("comparisonGrid");
        comparisonGrid.innerHTML = "";

        const versions = ["P1", "P2", "P3"];
        versions.forEach(vid => {
            const vData = data.comparison[vid];
            const parsed = vData.parsed;
            const meta = vData.metadata;

            const col = document.createElement("div");
            col.className = "bg-white border rounded-xl shadow-sm overflow-hidden flex flex-col";

            let headerBg = "bg-slate-100 text-slate-800";
            let pillText = "P1 Baseline";
            if (vid === "P2") {
                headerBg = "bg-sky-50 text-sky-900 border-b border-sky-100";
                pillText = "P2 Improved";
            } else if (vid === "P3") {
                headerBg = "bg-indigo-900 text-white";
                pillText = "P3 Final Optimized (Target)";
            }

            const isJsonValidBadge = vData.is_valid_json 
                ? `<span class="bg-emerald-100 text-emerald-700 text-[10px] px-2 py-0.5 rounded-full font-bold">Valid JSON</span>`
                : `<span class="bg-rose-100 text-rose-700 text-[10px] px-2 py-0.5 rounded-full font-bold">Unstructured Text</span>`;

            col.innerHTML = `
                <div class="p-3.5 ${headerBg} flex items-center justify-between">
                    <div>
                        <div class="font-bold text-sm flex items-center space-x-2">
                            <span>${pillText}</span>
                            ${isJsonValidBadge}
                        </div>
                        <p class="text-xs opacity-80 mt-0.5 line-clamp-1">${meta.name}</p>
                    </div>
                    <span class="text-xs font-mono opacity-80">${vData.execution_time_ms} ms</span>
                </div>
                <div class="p-4 flex-1 space-y-4 text-xs">
                    <div>
                        <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Overall Assessment</span>
                        <p class="mt-1 text-slate-800">${escapeHtml(parsed.overall_assessment)}</p>
                    </div>
                    <div>
                        <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Detected Issues (${parsed.issues.length})</span>
                        <div class="mt-1 space-y-2">
                            ${parsed.issues.map(iss => `
                                <div class="p-2 rounded bg-slate-50 border border-slate-200">
                                    <div class="flex justify-between items-center mb-1">
                                        <span class="font-semibold text-slate-800 truncate">${escapeHtml(iss.issue)}</span>
                                        <span class="px-1.5 py-0.2 rounded text-[10px] font-bold ${getSeverityBadgeClass(iss.severity)}">${escapeHtml(iss.severity)}</span>
                                    </div>
                                    <p class="text-slate-600">${escapeHtml(iss.explanation)}</p>
                                    <div class="mt-1.5 p-1.5 rounded bg-sky-50 text-sky-900 font-mono text-[11px]">
                                        <b>Hint:</b> ${escapeHtml(iss.hint)}
                                    </div>
                                </div>
                            `).join("")}
                        </div>
                    </div>
                    <div>
                        <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Positive Feedback</span>
                        <p class="mt-1 text-slate-700">${escapeHtml(parsed.positive_feedback)}</p>
                    </div>
                    <div>
                        <span class="font-bold text-slate-500 uppercase tracking-wider text-[10px]">Next Learning Step</span>
                        <p class="mt-1 text-slate-700">${escapeHtml(parsed.next_step)}</p>
                    </div>
                </div>
            `;
            comparisonGrid.appendChild(col);
        });

        comparisonContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // Export Reports
    exportMdBtn.addEventListener("click", () => triggerExport("markdown"));
    exportPdfBtn.addEventListener("click", () => triggerExport("pdf"));

    async function triggerExport(format) {
        if (!currentAnalysis) {
            showNotification("No analysis available to export.", "warning");
            return;
        }

        try {
            showNotification(`Generating ${format.toUpperCase()} report...`, "info");
            const payload = {
                format: format,
                code: codeEditor.value,
                student_id: "Student_C4",
                problem_description: problemDesc.value,
                analysis: currentAnalysis
            };

            const response = await fetch("/api/export-report", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!response.ok) throw new Error("Report export failed.");

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.style.display = "none";
            a.href = url;
            a.download = `CodeSense_Report_${Date.now()}.${format === "pdf" ? "pdf" : "md"}`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            showNotification(`Downloaded ${format.toUpperCase()} report!`, "success");
        } catch (err) {
            console.error("Export error:", err);
            showNotification(`Failed to export report: ${err.message}`, "error");
        }
    }

    // Helper functions
    function getSeverityBadgeClass(sev) {
        switch (sev) {
            case "Critical": return "badge-critical";
            case "High": return "badge-high";
            case "Medium": return "badge-medium";
            case "Low": return "badge-low";
            case "No issue detected": return "badge-clean";
            default: return "badge-medium";
        }
    }

    function escapeHtml(text) {
        if (!text) return "";
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    function showNotification(message, type = "info") {
        const toast = document.createElement("div");
        let bg = "bg-slate-800 text-white";
        if (type === "success") bg = "bg-emerald-600 text-white";
        if (type === "warning") bg = "bg-amber-600 text-white";
        if (type === "error") bg = "bg-rose-600 text-white";

        toast.className = `fixed bottom-5 right-5 z-50 px-4 py-2.5 rounded-lg shadow-xl text-sm font-medium flex items-center space-x-2 transition-all transform translate-y-2 opacity-0 ${bg}`;
        toast.innerHTML = `<span>${type === "success" ? "✓" : (type === "error" ? "✕" : "ℹ")}</span><span>${message}</span>`;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.classList.remove("translate-y-2", "opacity-0");
        }, 50);

        setTimeout(() => {
            toast.classList.add("translate-y-2", "opacity-0");
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    }
});
