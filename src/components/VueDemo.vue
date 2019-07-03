<template>
    <div>
        <button @click="run">RUN</button>
        <div id="result">
            <result-chart :datasets="datasets"></result-chart>
        </div>
    </div>
</template>

<script>
    import ResultChart from "./ResultChart";

    export default {
        name: 'VueDemo',
        components: {ResultChart},
        props: {},
        data() {
            return {
                datasets: [],
                colors: [
                    '#69FFC0',
                    '#D5E879',
                    '#FFD391',
                    '#E87988',
                    '#9E7DFF',
                    '#EB24DD',
                    '#FF9238',
                    '#2466FF',
                    '#EBE91E',
                    '#0FFF96'
                ]
            }
        },
        methods: {
            getRandomColor() {
                const letters = '0123456789ABCDEF';
                let color = '#';
                for (let i = 0; i < 6; i++) {
                    color += letters[Math.floor(Math.random() * 16)];
                }
                return color;
            },
            async run() {
                const res = await fetch('http://localhost:8000/genetic/');
                const json = await res.json();

                const datasets = [];
                let i = 0;

                datasets.push({
                    data: [{
                        x: json.coordinates[0][0],
                        y: json.coordinates[0][1],
                    }],
                    borderColor: 'black',
                    borderWidth: 1,
                    pointBackgroundColor: 'black',
                    pointBorderColor: '#000',
                    pointRadius: 5,
                    pointHoverRadius: 5,
                    fill: false,
                    tension: 0,
                    showLine: true
                });

                for (const item of json.path) {
                    const data = [];
                    data.push({
                        x: json.coordinates[0][0],
                        y: json.coordinates[0][1],
                    });
                    for (const nb of item) {
                        const point = json.coordinates[nb];
                        data.push({
                            x: point[0],
                            y: point[1]
                        })
                    }
                    data.push({
                        x: json.coordinates[0][0],
                        y: json.coordinates[0][1],
                    });

                    const color = i < this.colors.length ? this.colors[i] : this.getRandomColor();
                    datasets.push({
                        data: data,
                        borderColor: color,
                        borderWidth: 1,
                        pointBackgroundColor: color,
                        pointBorderColor: '#000',
                        pointRadius: 5,
                        pointHoverRadius: 5,
                        fill: false,
                        tension: 0,
                        showLine: true
                    });
                    i += 1;
                }
                this.datasets = datasets;
            }
        },
        created() {
            this.run();
        }
    }
</script>

<style scoped>
    #result {
        width: 500px;
        height: 500px;
    }
</style>
