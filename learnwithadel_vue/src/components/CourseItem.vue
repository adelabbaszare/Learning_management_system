<template>
    <div class="card is-fullheight">
        <div class="card-image">
            <figure class="image is-4by3">
                <img src="https://bulma.io/assets/images/placeholders/1280x960.png">
            </figure>
        </div>

        <div class="card-content">
            <div class="media">
                <div class="media-content">
                    <p class="is-size-5">{{ course.title }}</p>
                </div>
            </div>

            <div class="content">
                <p>{{ course.short_description }}</p>
                <router-link :to="{name: 'Course', params: {slug: course.slug}}">More...</router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['course']
}
</script>