<script context="module">
    export async function load({ fetch, params }) {
        // await new Promise(resolve => setTimeout(resolve, 1000)) // väntar 1 sekund. för att visa en delay för att hämta data
        const id = params.id // id är parameternamnet från filens namn
        // const res = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`)
        const res = await fetch(`/guides/${id}.json`)
        const { guide } = await res.json()

        if (res.ok) {
            return {
                props: {
                    guide // om nyckel har samma namn som variabel högre upp, används variabeln automatiskt som värde
                }
            }
        }
        return {
            status: 301,
            redirect: "/guides"
        }
    }
</script>
<script>
    export let guide
</script>

<div class="guide">
    <h2>{guide.title}</h2>
    <p>{guide.body}</p>
</div>

<style>
    .guide {
        margin-top: 40px;
        padding: 10px;
        border: 1px dotted rgba(255,255,255,0.2);
    }
</style>