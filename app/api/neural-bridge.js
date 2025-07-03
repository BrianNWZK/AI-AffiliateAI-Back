import express from "express";
const app = express();
app.use(express.json());

const activities = [];

function addActivity(type, payload = {}) {
  activities.unshift({ type, ...payload, timestamp: Date.now() });
  if (activities.length > 20) activities.length = 20;
}

app.get("/neural/metrics", (req, res) => {
  res.json({
    globalAnalysis: "Processing 2.3M data points",
    automationLevel: 87,
    marketTrends: [
      { region: "North America", growth: 12.5, status: "bullish" },
      { region: "Europe", growth: 8.3, status: "stable" },
      { region: "Asia Pacific", growth: 15.7, status: "bullish" },
    ],
    timestamp: new Date().toISOString(),
  });
  addActivity("metrics-served");
});

app.post("/neural/optimize", (req, res) => {
  addActivity("optimize-triggered", req.body);
  res.json({ success: true, message: "Neural optimization started!" });
});

app.get("/neural/activities", (req, res) => {
  res.json({ activities });
});

const PORT = process.env.PORT || 3003;
app.listen(PORT, () => {
  console.log(`Neural Bridge running on port ${PORT}`);
});
