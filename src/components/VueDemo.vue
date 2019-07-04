<template>
    <div class="level tile is-ancestor">
        <div class="tile is-12 is-parent">
            <section class="section level-item level-left tile is-parent">
                <div class="tile is-child box" id="controls">
                    <b-field label="Points" class="center-div">
                        <b-numberinput v-model="points" min="1" controls-position="compact"></b-numberinput>
                    </b-field>
                    <b-field label="Capacity" class="center-div">
                        <b-numberinput v-model="capacity" min="1" controls-position="compact"></b-numberinput>
                    </b-field>
                    <b-field label="Individuals" class="center-div">
                        <b-numberinput v-model="individuals" min="1" controls-position="compact"></b-numberinput>
                    </b-field>
                    <b-field label="Replace" class="center-div">
                        <b-numberinput v-model="replace" min="0" controls-position="compact"></b-numberinput>
                    </b-field>
                    <b-field label="Generations" class="center-div">
                        <b-numberinput v-model="generations" min="1" controls-position="compact"></b-numberinput>
                    </b-field>
                    <b-button @click="run" :loading="running" type="is-primary">RUN</b-button>
                </div>
            </section>
            <section class="section level-item level-right tile is-parent">
                <div class="tile is-child box" id="resultcontainer">
                    <div id="result">
                        <result-chart :datasets="datasets"></result-chart>
                    </div>
                </div>
            </section>
        </div>
    </div>
</template>

<script>
    import ResultChart from "./ResultChart";
    import BButton from "buefy/src/components/button/Button";

    export default {
        name: 'VueDemo',
        components: {BButton, ResultChart},
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
                ],
                running: false,
                points: 100,
                capacity: 10,
                individuals: 50,
                replace: 25,
                generations: 500,
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
                if (this.running) return;

                this.running = true;

                const url = new URL("http://localhost:8000/genetic");
                const params = {
                    capacity: this.capacity,
                    points: this.points,
                    individuals: this.individuals,
                    replace: this.replace,
                    generations: this.generations
                };
                Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

                const res = await fetch(url);
                const json = await res.json();

                const datasets = [];
                let i = 0;

                datasets.push({
                    data: [{
                        x: json.coordinates[0][0],
                        y: json.coordinates[0][1],
                    }],
                    borderColor: '#aeaeae',
                    borderWidth: 1,
                    pointBackgroundColor: '#000',
                    pointBorderColor: '#000',
                    pointRadius: 8,
                    pointHoverRadius: 8,
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
                this.running = false;
            }
        },
        created() {
            this.run();
        }
    }
</script>

<style scoped>
    #resultcontainer {
        display: flex;
        align-items: center;
        justify-content: center;
    }

    #result {
        width: 500px;
        height: 500px;
    }

    #controls {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
    }

    .center-div {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>
