import React from "react";
import { LineChart } from "@mui/x-charts";
import { Paper, Typography } from "@mui/material";

type HourlyDataPoint = {
    datetime: string;
    temperature_2m: number;
    precipitation_probability: number;
};

type ChartPoint = {
    time: number;
    temperature: number;
    precipitation: number;
};

interface WeatherForecastChartProps {
    data: { hourly_data: HourlyDataPoint[] };
}

const transformWeatherData = (hourlyData: HourlyDataPoint[]): ChartPoint[] =>
    hourlyData.map((entry) => ({
        time: new Date(entry.datetime).getTime(),
        temperature: entry.temperature_2m,
        precipitation: entry.precipitation_probability,
    }));

const WeatherForecastChart: React.FC<WeatherForecastChartProps> = ({ data }) => {
    const chartData = transformWeatherData(data.hourly_data);

    return (
        <Paper elevation={3} sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
                Прогноз погоды по часам
            </Typography>

            <LineChart
                dataset={chartData}
                height={400}
                width={850}
                xAxis={[
                    {
                        dataKey: "time",
                        label: "Время",
                        valueFormatter: (timestamp: string) =>
                            new Date(timestamp).toLocaleDateString("ru-RU", {
                                day: "numeric",
                                month: "short",
                                hour: "numeric",
                                minute: "numeric",
                            }),
                    },
                ]}
                yAxis={[
                    {
                        id: "left",
                        label: "Температура (°C)",
                        min: Math.min(...chartData.map((d) => d.temperature)) - 5,
                        max: Math.max(...chartData.map((d) => d.temperature)) + 5,
                        position: "left",
                    },
                    {
                        id: "right",
                        label: "Вероятность осадков (%)",
                        min: 0,
                        max: 100,
                        position: "right",
                    },
                ]}
                series={[
                    {
                        dataKey: "temperature",
                        label: "Температура °C",
                        color: "#1976d2",
                        yAxisId: "left",
                        showMark: false,
                    },
                    {
                        dataKey: "precipitation",
                        label: "Вероятность осадков %",
                        color: "#ef5350",
                        yAxisId: "right",
                        showMark: false,
                    },
                ]}
            />
        </Paper>
    );
};

export default WeatherForecastChart;
