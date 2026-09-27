const input = document.getElementById("queryInput");
const analyze = document.getElementById("analyzeBtn");
const clear = document.getElementById("clearBtn");
const count = document.getElementById("charCount");

const empty = document.getElementById("empty");
const loading = document.getElementById("loading");
const result = document.getElementById("result");
const badge = document.getElementById("badge");

const category = document.getElementById("category");
const confidence = document.getElementById("confidence");
const bar = document.getElementById("bar");

const decision = document.getElementById("decision");
const decisionIcon = document.getElementById("decisionIcon");
const decisionLabel = document.getElementById("decisionLabel");
const decisionDetail = document.getElementById("decisionDetail");

const queueName = document.getElementById("queueName");
const queueNote = document.getElementById("queueNote");
const topPredictions = document.getElementById("topPredictions");


// ============================================================
// HISTORY
// ============================================================

const HISTORY_KEY = "smartroute_history_v1";

let history = [];

try {
    history = JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");

    if (!Array.isArray(history)) {
        history = [];
    }
} catch (error) {
    console.warn("Could not load routing history:", error);
    history = [];
}


// ============================================================
// SERVICE QUEUE MAPPING
// ============================================================

function queueFromIntent(label) {

    const l = String(label).toLowerCase();

    // --------------------------------------------------------
    // Card & Payment Support
    // --------------------------------------------------------

    if (
        l.includes("transaction_charged_twice") ||
        l.includes("transaction charged twice") ||
        l.includes("card_payment") ||
        l.includes("card payment") ||
        l.includes("cash_withdrawal") ||
        l.includes("cash withdrawal") ||
        l.includes("card_") ||
        l.includes("cash_") ||
        l.includes("atm") ||
        l.includes("declined_cash") ||
        l.includes("cash withdrawal") ||
        l.includes("cash withdrawal charge")
    ) {
        return "Card & Payment Support";
    }


    // --------------------------------------------------------
    // Transfers & Payments
    // --------------------------------------------------------

    if (
        l.includes("transfer") ||
        l.includes("beneficiary")
    ) {
        return "Transfers & Payments";
    }


    // --------------------------------------------------------
    // Top-Up Services
    // --------------------------------------------------------

    if (
        l.includes("top_up") ||
        l.includes("top up") ||
        l.includes("cash deposit")
    ) {
        return "Top-Up Services";
    }


    // --------------------------------------------------------
    // Currency & Exchange
    // --------------------------------------------------------

    if (
        l.includes("exchange") ||
        l.includes("currency")
    ) {
        return "Currency & Exchange";
    }


    // --------------------------------------------------------
    // Account & Verification
    // --------------------------------------------------------

    if (
        l.includes("identity") ||
        l.includes("passcode") ||
        l.includes("age_limit") ||
        l.includes("age limit") ||
        l.includes("verify") ||
        l.includes("verification")
    ) {
        return "Account & Verification";
    }


    // --------------------------------------------------------
    // Account Services
    // --------------------------------------------------------

    if (
        l.includes("account") ||
        l.includes("personal")
    ) {
        return "Account Services";
    }


    // --------------------------------------------------------
    // Default
    // --------------------------------------------------------

    return "General Customer Support";
}


// ============================================================
// SAVE HISTORY
// ============================================================

function saveHistory(item) {

    history.unshift(item);

    // Keep maximum 50 entries
    history = history.slice(0, 50);

    localStorage.setItem(
        HISTORY_KEY,
        JSON.stringify(history)
    );

    renderAnalytics();
}


// ============================================================
// ANALYTICS
// ============================================================

function renderAnalytics() {

    const total = history.length;

    const auto = history.filter(
        x => x.level === "high"
    ).length;

    const medium = history.filter(
        x => x.level === "medium"
    ).length;

    const low = history.filter(
        x => x.level === "low"
    ).length;

    const review = medium + low;

    const avg =
        total > 0
            ? history.reduce(
                (sum, x) => sum + Number(x.confidence || 0),
                0
            ) / total
            : 0;


    // --------------------------------------------------------
    // KPI cards
    // --------------------------------------------------------

    const totalQueries =
        document.getElementById("totalQueries");

    const autoRouted =
        document.getElementById("autoRouted");

    const needsReview =
        document.getElementById("needsReview");

    const avgConfidence =
        document.getElementById("avgConfidence");


    if (totalQueries) {
        totalQueries.textContent = total;
    }

    if (autoRouted) {
        autoRouted.textContent = auto;
    }

    if (needsReview) {
        needsReview.textContent = review;
    }

    if (avgConfidence) {
        avgConfidence.textContent =
            `${avg.toFixed(1)}%`;
    }


    // --------------------------------------------------------
    // Decision distribution
    // --------------------------------------------------------

    renderBars(
        "decisionBars",
        [
            [
                "Auto Route",
                auto,
                "high"
            ],
            [
                "Route + Review",
                medium,
                "medium"
            ],
            [
                "Human Review",
                low,
                "low"
            ]
        ]
    );


    // --------------------------------------------------------
    // Service queue distribution
    // --------------------------------------------------------

    const queues = {};

    history.forEach(item => {

        const queue =
            item.queue || "General Customer Support";

        queues[queue] =
            (queues[queue] || 0) + 1;
    });


    const queueItems =
        Object.entries(queues)
            .sort((a, b) => b[1] - a[1])
            .slice(0, 6)
            .map(item => [
                item[0],
                item[1],
                ""
            ]);


    renderBars(
        "queueBars",
        queueItems
    );


    // --------------------------------------------------------
    // Recent routing history
    // --------------------------------------------------------

    const body =
        document.getElementById("historyBody");

    if (!body) {
        return;
    }


    if (!history.length) {

        body.innerHTML =
            '<tr><td colspan="6" class="no-data">' +
            'No queries analyzed yet.' +
            '</td></tr>';

        return;
    }


    body.innerHTML = history.map(item => {

        const confidenceValue =
            Number(item.confidence || 0);

        return `
            <tr>

                <td>
                    ${escapeHtml(item.time || "")}
                </td>

                <td
                    class="query-cell"
                    title="${escapeHtml(item.query || "")}"
                >
                    ${escapeHtml(item.query || "")}
                </td>

                <td>
                    ${escapeHtml(item.intent || "")}
                </td>

                <td>
                    ${confidenceValue.toFixed(2)}%
                </td>

                <td>
                    <span class="pill ${escapeHtml(item.level || "")}">
                        ${escapeHtml(item.decision || "")}
                    </span>
                </td>

                <td>
                    ${escapeHtml(
            item.queue ||
            "General Customer Support"
        )}
                </td>

            </tr>
        `;

    }).join("");
}


// ============================================================
// ANALYTICS BAR RENDERING
// ============================================================

function renderBars(id, items) {

    const el =
        document.getElementById(id);

    if (!el) {
        return;
    }


    if (!items.length) {

        el.innerHTML =
            '<div class="no-data">No data yet.</div>';

        return;
    }


    const max =
        Math.max(
            ...items.map(item => item[1]),
            1
        );


    el.innerHTML = items.map(item => {

        const percentage =
            (item[1] / max) * 100;

        return `
            <div class="bar-row">

                <span>
                    ${escapeHtml(item[0])}
                </span>

                <div class="bar-track">
                    <div
                        class="bar-fill"
                        style="width:${percentage}%"
                    ></div>
                </div>

                <b>
                    ${item[1]}
                </b>

            </div>
        `;

    }).join("");
}


// ============================================================
// CHARACTER COUNTER
// ============================================================

input.addEventListener(
    "input",
    () => {

        count.textContent =
            `${input.value.length} / 1000`;

    }
);


// ============================================================
// CLEAR CURRENT QUERY
// ============================================================

clear.addEventListener(
    "click",
    () => {

        input.value = "";

        count.textContent =
            "0 / 1000";

        result.classList.add("hidden");

        loading.classList.add("hidden");

        empty.classList.remove("hidden");

        badge.textContent =
            "WAITING";

        bar.style.width =
            "0%";

        input.focus();
    }
);


// ============================================================
// EXAMPLE QUERY BUTTONS
// ============================================================

document
    .querySelectorAll(".examples button")
    .forEach(button => {

        button.addEventListener(
            "click",
            () => {

                input.value =
                    button.textContent;

                input.dispatchEvent(
                    new Event("input")
                );

                input.focus();
            }
        );

    });


// ============================================================
// MAIN PREDICTION
// ============================================================

async function runPrediction() {

    const text =
        input.value.trim();


    // Empty query
    if (!text) {

        input.focus();

        return;
    }


    // --------------------------------------------------------
    // UI: Loading
    // --------------------------------------------------------

    empty.classList.add("hidden");

    result.classList.add("hidden");

    loading.classList.remove("hidden");

    badge.textContent =
        "ANALYZING";

    analyze.disabled =
        true;


    try {

        // ----------------------------------------------------
        // Send query to Flask backend
        // ----------------------------------------------------

        const response =
            await fetch(
                "/api/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        text: text
                    })
                }
            );


        const data =
            await response.json();


        if (
            !response.ok ||
            !data.success
        ) {

            throw new Error(
                data.error ||
                "Prediction failed."
            );
        }


        // ----------------------------------------------------
        // Prediction
        // ----------------------------------------------------

        category.textContent =
            data.display_category;


        const confidenceValue =
            Number(data.confidence || 0);


        confidence.textContent =
            `${confidenceValue.toFixed(2)}%`;


        bar.style.width =
            `${Math.min(
                Math.max(confidenceValue, 0),
                100
            )}%`;


        // ----------------------------------------------------
        // Routing decision
        //
        // IMPORTANT:
        // Flask determines the routing level.
        // The frontend only displays it.
        // ----------------------------------------------------

        const level =
            data.routing.level;


        decision.className =
            `decision ${level}`;


        if (level === "high") {

            decisionIcon.textContent =
                "✓";

        } else if (level === "medium") {

            decisionIcon.textContent =
                "!";

        } else {

            decisionIcon.textContent =
                "↗";
        }


        decisionLabel.textContent =
            data.routing.label;


        decisionDetail.textContent =
            data.routing.detail;


        // ----------------------------------------------------
        // Service queue
        // ----------------------------------------------------

        const queue =
            queueFromIntent(
                data.category
            );


        queueName.textContent =
            queue;


        queueNote.textContent =
            `Primary intent: ${data.display_category}`;


        // ----------------------------------------------------
        // Top predictions
        // ----------------------------------------------------

        if (
            Array.isArray(
                data.top_predictions
            )
        ) {

            topPredictions.innerHTML =
                data.top_predictions
                    .map(item => {

                        return `
                            <div class="alt">

                                <span>
                                    ${escapeHtml(
                            item.display_category
                        )}
                                </span>

                                <span>
                                    ${Number(
                            item.confidence || 0
                        ).toFixed(2)}%
                                </span>

                            </div>
                        `;

                    })
                    .join("");

        } else {

            topPredictions.innerHTML = "";
        }


        // ----------------------------------------------------
        // Save history
        // ----------------------------------------------------

        saveHistory({

            time:
                new Date().toLocaleTimeString(
                    [],
                    {
                        hour: "2-digit",
                        minute: "2-digit"
                    }
                ),

            query:
                text,

            intent:
                data.display_category,

            confidence:
                confidenceValue,

            level:
                level,

            decision:
                data.routing.label,

            queue:
                queue
        });


        // ----------------------------------------------------
        // Show result
        // ----------------------------------------------------

        loading.classList.add("hidden");

        result.classList.remove("hidden");

        badge.textContent =
            "ROUTED";


        // Scroll dashboard into view
        const dashboard =
            document.querySelector(
                ".dashboard"
            );

        if (dashboard) {

            dashboard.scrollIntoView({
                behavior: "smooth",
                block: "start"
            });
        }


    } catch (error) {

        console.error(
            "Prediction error:",
            error
        );


        loading.classList.add("hidden");

        empty.classList.remove("hidden");

        badge.textContent =
            "ERROR";


        alert(
            error.message ||
            "Something went wrong."
        );


    } finally {

        analyze.disabled =
            false;
    }
}


// ============================================================
// HTML ESCAPING
// ============================================================

function escapeHtml(value) {

    return String(value)
        .replaceAll(
            "&",
            "&amp;"
        )
        .replaceAll(
            "<",
            "&lt;"
        )
        .replaceAll(
            ">",
            "&gt;"
        )
        .replaceAll(
            '"',
            "&quot;"
        )
        .replaceAll(
            "'",
            "&#039;"
        );
}


// ============================================================
// ANALYZE BUTTON
// ============================================================

analyze.addEventListener(
    "click",
    runPrediction
);


// ============================================================
// CTRL + ENTER
// ============================================================

input.addEventListener(
    "keydown",
    event => {

        if (
            (event.ctrlKey || event.metaKey) &&
            event.key === "Enter"
        ) {

            event.preventDefault();

            runPrediction();
        }
    }
);


// ============================================================
// CLEAR ALL HISTORY
// ============================================================

const clearHistoryButton =
    document.getElementById(
        "clearHistory"
    );


if (clearHistoryButton) {

    clearHistoryButton.addEventListener(
        "click",
        () => {

            if (
                confirm(
                    "Clear all routing history from this browser?"
                )
            ) {

                history = [];

                localStorage.removeItem(
                    HISTORY_KEY
                );

                renderAnalytics();
            }
        }
    );
}


// ============================================================
// INITIAL RENDER
// ============================================================

renderAnalytics();