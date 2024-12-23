import React, { useState, useEffect } from "react";
import PopularPanel from "./PopularPanel";

const PopularPage = () => {
  const [dailyData, setDailyData] = useState(null);
  const [weeklyData, setWeeklyData] = useState(null);
  const [monthlyData, setMonthlyData] = useState(null);

  const [loadingDaily, setLoadingDaily] = useState(true);
  const [loadingWeekly, setLoadingWeekly] = useState(true);
  const [loadingMonthly, setLoadingMonthly] = useState(true);

  useEffect(() => {
    // Fetch daily data
    fetch("http://localhost:8000/popular-rank/daily", {
      method: "POST",
      headers: { accept: "application/json" },
    })
      .then((res) => res.json())
      .then((data) => {
        setDailyData(data);
        setLoadingDaily(false);
      })
      .catch((error) => console.error("Error fetching daily data:", error));

    // Fetch weekly data
    fetch("http://localhost:8000/popular-rank/weekly", {
      method: "POST",
      headers: { accept: "application/json" },
    })
      .then((res) => res.json())
      .then((data) => {
        setWeeklyData(data);
        setLoadingWeekly(false);
      })
      .catch((error) => console.error("Error fetching weekly data:", error));

    // Fetch monthly data
    fetch("http://localhost:8000/popular-rank/monthly", {
      method: "POST",
      headers: { accept: "application/json" },
    })
      .then((res) => res.json())
      .then((data) => {
        setMonthlyData(data);
        setLoadingMonthly(false);
      })
      .catch((error) => console.error("Error fetching monthly data:", error));
  }, []);

  return (
    <div className="container mt-4">
      <div className="row">
        {/* Daily Panel */}
        <div className="col-md-4">
          <PopularPanel title="Daily Popular Articles" data={dailyData} loading={loadingDaily} />
        </div>
        {/* Weekly Panel */}
        <div className="col-md-4">
          <PopularPanel title="Weekly Popular Articles" data={weeklyData} loading={loadingWeekly} />
        </div>
        {/* Monthly Panel */}
        <div className="col-md-4">
          <PopularPanel title="Monthly Popular Articles" data={monthlyData} loading={loadingMonthly} />
        </div>
      </div>
    </div>
  );
};

export default PopularPage;
