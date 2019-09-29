#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.utils.safestring import mark_safe

__author__ = "HubLive"


class Pagination(object):
    def __init__(self, request, all_count, max_show=7, per_num=2, ):
        #
        self.base_url = request.path_info

        # 查询条件
        # 获取当前页码
        try:
            self.current_page = int(request.GET.get('page', 1))
            if self.current_page <= 0:
                self.current_page = 1
        except Exception as e:
            self.current_page = 1
        # 最大显示页码数
        self.max_show = max_show
        half_show = max_show // 2
        
        # 每页显示的数据条数
        self.per_num = per_num
        
        # 总数据量
        self.all_count = all_count
        
        # 总页码数
        self.total_num, more = divmod(all_count, per_num)
        if more:
            self.total_num += 1
        
        # 总页码数小于最大显示数：显示总页码数
        if self.total_num <= max_show:
            self.page_start = 1
            self.page_end = self.total_num
        else:
            # 总页码数大于最大显示数
            if self.current_page <= half_show:
                self.page_start = 1
                self.page_end = max_show
            elif self.current_page + half_show >= self.total_num:
                self.page_end = self.total_num
                self.page_start = self.total_num - max_show + 1
            else:
                self.page_start = self.current_page - half_show
                self.page_end = self.current_page + half_show
    
    @property
    def start(self):
        return (self.current_page - 1) * self.per_num
    
    @property
    def end(self):
        return self.current_page * self.per_num
    
    def show_li(self):
        # 存放li标签列表
        html_list = []
        
        if self.current_page == 1:
            prev_li = '<li  class="disabled paginate_button page-item"><a href="#" class="page-link">首页</a></li>'
        else:
            prev_li = '<li class="paginate_button page-item"><a href="{1}?page={0}" class="page-link">上一页</a></li>'.format(self.current_page - 1, self.base_url)
        html_list.append(prev_li)
        for num in range(self.page_start, self.page_end + 1):
            if self.current_page == num:
                li_html = '<li class="paginate_button page-item active"><a href="{1}?page={0}" class="page-link">{0}</a></li>'.format(num, self.base_url)
            else:
                li_html = '<li class="paginate_button page-item"><a href="{1}?page={0}" class="page-link">{0}</a></li>'.format(num, self.base_url)
            html_list.append(li_html)
        if self.current_page == self.total_num:
            next_li = '<li class="disabled paginate_button page-item"><a href="#" class="page-link">尾页</a></li>'
        else:
            next_li = '<li class="paginate_button page-item"> <a href="{1}?page={0}" class="page-link">下一页</a></li>'.format(self.current_page + 1, self.base_url)
        html_list.append(next_li)
        return mark_safe(''.join(html_list))
