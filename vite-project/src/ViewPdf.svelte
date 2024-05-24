<script>
    import { onMount } from 'svelte';
    import { useParams } from 'svelte-navigator';
  
    const { filename } = useParams();
  
    onMount(() => {
      const pdfUrl = `http://127.0.0.1:5000/view_project_report/${filename}`;
      window.location.href = pdfUrl;
    });
</script>
  
<div>Loading PDF...</div>
  