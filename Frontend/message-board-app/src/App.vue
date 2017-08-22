<template>
  <div id="app">
    <div class="container">
      <h1 class="title">Message Board</h1>
        <!-- prevent 表示阻止表单提交时重载页面 -->
        <!-- keydown 绑定的事件表示表单下的某个数据框有字符输入时，清除该输入框上的errors -->
        <form action="/api/messages" method="POST" @submit.prevent="addMessage" @keydown="errors.clear($event.target.name)">
          <!-- 设置 has-error 类，设置了这个类 div 里面都会显示错误的状态，如输入框边框会变红色，help-block 里的文字也会变红色 -->
          <!-- from-group 是必要的类，是否设置 has-error 需要看 errors 中是否有该输入框的错误，这是 vue 类绑定语法中的一个 -->
          <div :class="['form-group', {'has-error': errors.has('name')}]">
            <input type="text" class="form-control" name="name" placeholder="Name" v-model="name">
            <span class="help-block" v-if="errors.has('name')" v-text="errors.get('name')"></span>
          </div>
          <div :class="['form-group', {'has-error': errors.has('text')}]">
            <textarea class="form-control" name="text" rows="5" placeholder="Say something..." v-model="text"></textarea>
            <span class="help-block" v-text="errors.get('text')"></span>
          </div>
          <!--当 errors 中有任何一个输入框有错误时，设置 Submit 按钮为 disabled 状态-->
          <button class="btn btn-default" :disabled="errors.any()">Submit</button>
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
var axios = require('axios')

// 将 errors 相关操作封装成为一个类，使代码开起来更清晰
class Errors {
  constructor() {
    this.errors = { }
  }

  // 某个输入框数据是否有错误
  has(field) {
    return this.errors.hasOwnProperty(field)
  }

  // 任何一个输入框数据有错误返回true
  any() {
    return Object.keys(this.errors).length > 0
  }

  // 获取输入框的第一个错误（每个输入框的错误是个列表）
  get(field) {
    if (this.errors[field]) {
      return this.errors[field][0]
    }
  }

  // 初始化 errors
  record(errors) {
    this.errors = errors
  }

  // 清除某个输入框的错误
  clear(field) {
    delete this.errors[field]
  }
}

export default {
  name: 'app',
  data () {
    return {
      name: '',
      text: '',
      messages: [],
      errors: new Errors()
    }
  },
  methods: {
    // 点击 Submit 会触发此事件，向服务器发送 POST 请求
    addMessage() {
      axios.post('/api/messages', {
        'name': this.name,
        'text': this.text
      }).then(response => {
        if (response.data.ok) {
          this.messages.unshift({
            'name': this.name,
            'text': this.text,
            'created_at': new Date().toISOString()
          })
          this.name = ''
          this.text = ''
        }
      // 当返回错误时，初始化 errors
      }).catch(error => this.errors.record(error.response.data.errors))
    }
  },
  mounted() {
    axios.get('/api/messages').then(response => this.messages = response.data)
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