class CopyrightEncryptor:
    @staticmethod
    def encrypt_html(text):
        # 构建HTML
        html = f'''
        <div class="copyright-info">
            {text}
        </div>
        '''
        return html

    @staticmethod 
    def get_copyright():
        text = '''
        <div class="text-center text-gray-500 text-sm">
            <p onclick='window.location.href="https://github.com/stormwasd/LI-CMS"'>© 2025 LI-CMS 版权所有</p>
        </div>
        '''
        return CopyrightEncryptor.encrypt_html(text) 