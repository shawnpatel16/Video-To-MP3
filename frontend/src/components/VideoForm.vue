<template>
  <div>
    <input type="text" v-model="youtubeLink" placeholder="Enter YouTube Link">

    <div v-for="(timestamp, index) in timestamps" :key="index">
      <input type="text" v-model="timestamp.start" placeholder="Start Timestamp">
      <input type="text" v-model="timestamp.end" placeholder="End Timestamp">
    </div>

    <button @click="addTimestamp">Add More Timestamps</button>

    <button @click="submit">Submit</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      youtubeLink: '',
      timestamps: [{ start: '', end: '' }]
    }
  },
  methods: {
    addTimestamp() {
      this.timestamps.push({ start: '', end: '' })
    },
    async submit() {
      const response = await axios.post('http://localhost:8000/api/convert', {
        youtubeLink: this.youtubeLink,
        timestamps: this.timestamps
      })
      console.log(response)
    }
  }
}
</script>
