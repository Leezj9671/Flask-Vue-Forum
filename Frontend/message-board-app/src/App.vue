<template>
  <div id="app">
    <div class="container">
      <h1 class="title">Message Board</h1>
        <form action="/api/messages" method="POST" @submit.prevent="onSubmit">
          <div class="form-group">
            <input type="text" class="form-control" name="name" placeholder="Name" v-model="name">
          </div>
          <div class="form-group">
            <textarea class="form-control" rows="5" placeholder="Say something..." v-model="text"></textarea>
          </div>
          <button class="btn btn-default">Submit</button>
        </form>
        <div class="messages-header">{{ messages.length }} messages</div>
        <div class="messages">
          <ul tansition="fade">
            <template v-for="message in messages">
              <message-item :message="message"></message-item>
            </template>
          </ul>
        </div>
    </div>
  </div>
</template>
<script>
import MessageItem from './components/MessageItem.vue'

export default {
  name: 'app',
  data () {
    return {
      name: '',
      text: '',

      // ????
      messages: [
        {name: 'Abbb', text: 'testtext1', created_at: '2017-06-29T11:04:52.226Z'},
        {name: 'Bddd', text: 'testtext2', created_at: '2017-06-19T11:04:52.226Z'},
        {name: 'Zddd', text: 'testtext3', created_at: '2017-06-09T11:04:52.226Z'},
      ]
    }
  },
  methods: {
    onSubmit() {
      this.messages.unshift({
        name: this.name,
        text: this.text,
        created_at: new Date().toISOString()
      })
      this.name = ''
      this.text = ''
    }
  },
  components: {
    MessageItem
  }
}
</script>
<style>
.container {
  width: 650px;
  margin-top: 60px;
}

#app {
  margin-top: 60px;
  margin: 0 auto;
}

.title {
  text-align: center;
  margin-bottom: 20px;
  color: #e3e3e3;
}

.messages-header {
  line-height: 1;
  color: #666;
  padding: 20px 0 6px;
  border-bottom: 1px solid #eee;
  text-transform: uppercase;
  font-size: 13px;
}

.messages ul {
  margin: 0;
  padding: 0;
}
</style>