<template>
  <div>
    <input type="text" v-model="youtubeLink" placeholder="Enter YouTube Link">

    <div v-for="(timestamp, index) in timestamps" :key="index">
      <input type="text" v-model="timestamp.start" placeholder="Start Timestamp">
      <input type="text" v-model="timestamp.end" placeholder="End Timestamp">
    </div>

    <button @click="addTimestamp">Add More Timestamps</button>

    <button @click="convertAndDownload">Submit</button>
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
    convertAndDownload() {
        axios({
            url: 'http://localhost:8000/api/convert',
            method: 'POST',
            data: {
                youtubeLink: this.youtubeLink,
                timestamps: this.timestamps,
            },
            responseType: 'blob', 
        }).then((response) => {
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
          link.href = url;
          const contentDisposition = String(response.headers['content-disposition']);
            let fileName = 'download.mp3';  
            if (contentDisposition) {
              const fileNameMatch = contentDisposition.match(/attachment; filename=(.+)/);
                if (fileNameMatch.length === 2)
                    fileName = `${fileNameMatch[1]}.mp3`;
            }
            link.setAttribute('download', fileName);
            document.body.appendChild(link);
            link.click();
        });
    }
  }
}
</script>
