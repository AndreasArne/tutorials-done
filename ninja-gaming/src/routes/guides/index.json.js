
export async function get() {
    // connect to db & get data
    const guides = [
        { id: 1, title: "some title", body: "lorem ipsum" },
        { id: 2, title: "some title 2", body: "lorem ipsum"},
        { id: 3, title: "some title 3", body: "lorem ipsum"},
        { id: 4, title: "some title 4", body: "lorem ipsum"},
        { id: 5, title: "some title 5", body: "lorem ipsum" },
    ]
    return {
        status: 200,
        body: {guides}
    }
}