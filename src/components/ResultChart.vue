<script>
    import {Scatter} from 'vue-chartjs'

    export default {
        name: "ResultChart",
        extends: Scatter,
        props: ['datasets'],
        computed: {
            data() {
                return {
                    datasets: this.datasets,
                }
            }
        },
        data() {
            return {
                options: {
                    legend: false,
                    tooltips: false,
                    scales: {
                        xAxes: [{
                            ticks: {
                                min: 0,
                                max: 2000
                            },
                            gridLines: {
                                color: '#888',
                                drawOnChartArea: false
                            }
                        }],
                        yAxes: [{
                            ticks: {
                                min: 0,
                                max: 2000,
                                padding: 10
                            },
                            gridLines: {
                                color: '#888',
                                drawOnChartArea: false
                            }
                        }]
                    }
                },
            }
        },
        watch: {
            data: {
                handler: function (d) {
                    this.$data._chart.destroy();

                    this.renderChart(
                        this.data,
                        this.options
                    )
                },
                deep: true
            }
        },
        mounted() {
            this.renderChart(
                this.data,
                this.options
            )
        }
    }
</script>

<style scoped>

</style>