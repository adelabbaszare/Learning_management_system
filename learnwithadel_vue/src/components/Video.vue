<template>
<div class="video-container">
    <iframe
        title="YouTube video player"
        :src="'https://www.youtube.com/embed/' + youtube_id"
        width="100%"
        height="600"
        frameborder="5"
        marginwidth="5"
        style="border: none; border-radius: 16px; box-shadow: 0 8px 24px purple; overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease;"
        allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture;"
        allowfullscreen>
    </iframe>   
</div>
</template>

<script>
export default {
    props: ['youtube_id']
}
</script>