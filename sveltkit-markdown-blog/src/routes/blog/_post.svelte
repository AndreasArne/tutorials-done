<script>
  export let title
  export let date
  export let categories;
</script>

<svelte:head>
  <title>My blog - {title}</title>
  <meta property="og:title" content={title} />
</svelte:head>

<h1>{title}</h1>

<p>Published: {date}</p>

{#if categories.length}
  <aside>
    <h2>Posted in:</h2>
    <ul>
      {#each categories as category}
        <li>
          <a href="/blog/categories/{category}">
            {category}
          </a>
        </li>
      {/each}
    </ul>
  </aside>
{/if}
<slot />