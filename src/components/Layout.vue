<template>
  <el-container class="layout-container">
    <!-- Sidebar -->
    <el-aside :width="isCollapse ? '64px' : '220px'" class="sidebar">
      <div class="logo">
        <img v-if="!isCollapse" src="https://demo.crmeb.net/admin/img/logo.png" alt="logo" class="logo-full" />
        <img v-else src="https://demo.crmeb.net/admin/img/logo_small.png" alt="logo" class="logo-mini" />
      </div>
      <el-menu
        :default-active="route.path"
        class="el-menu-vertical"
        background-color="#001529"
        text-color="#a6adb4"
        active-text-color="#fff"
        :collapse="isCollapse"
        :collapse-transition="false"
        router
      >
  <el-sub-menu index="/product">
    <template #title>
      <el-icon><Menu /></el-icon>
      <span>商城</span>
    </template>
    <el-sub-menu index="/product">
      <template #title>
        <el-icon><Goods /></el-icon>
        <span>商品</span>
      </template>
      <el-menu-item index="/product_product_list">
        <el-icon><Goods /></el-icon>
        <span>商品列表</span>
      </el-menu-item>
      <el-menu-item index="/product_product_classify">
        <el-icon><Goods /></el-icon>
        <span>商品分类</span>
      </el-menu-item>
      <el-menu-item index="/product_add_product">
        <el-icon><Menu /></el-icon>
        <span>产品添加</span>
      </el-menu-item>
      <el-menu-item index="/product_product_attr">
        <el-icon><Goods /></el-icon>
        <span>商品规格</span>
      </el-menu-item>
      <el-menu-item index="/product_label">
        <el-icon><Goods /></el-icon>
        <span>商品标签</span>
      </el-menu-item>
      <el-sub-menu index="/product_product_brand">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>类目参数</span>
        </template>
        <el-menu-item index="/product_product_brand">
          <el-icon><Goods /></el-icon>
          <span>商品品牌</span>
        </el-menu-item>
        <el-menu-item index="/product_unitList">
          <el-icon><Goods /></el-icon>
          <span>商品单位</span>
        </el-menu-item>
        <el-menu-item index="/product_specs">
          <el-icon><Goods /></el-icon>
          <span>商品参数</span>
        </el-menu-item>
        <el-sub-menu index="/product_ensure">
          <template #title>
            <el-icon><Menu /></el-icon>
            <span>保障服务</span>
          </template>
          <el-menu-item index="/product_ensure_create">
            <el-icon><Goods /></el-icon>
            <span>添加商品参数模版</span>
          </el-menu-item>
        </el-sub-menu>
      </el-sub-menu>
      <el-sub-menu index="/setting_system_form">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>系统表单</span>
        </template>
        <el-menu-item index="/setting_system_create">
          <el-icon><Menu /></el-icon>
          <span>添加系统表单</span>
        </el-menu-item>
        <el-menu-item index="/setting_system_form_data">
          <el-icon><Menu /></el-icon>
          <span>系统表单收集数据</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/product_product_reply">
        <el-icon><Goods /></el-icon>
        <span>商品评论</span>
      </el-menu-item>
      <el-menu-item index="/product_product_reply_config">
        <el-icon><Setting /></el-icon>
        <span>评论设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/order">
      <template #title>
        <el-icon><List /></el-icon>
        <span>订单</span>
      </template>
      <el-sub-menu index="/order_list">
        <template #title>
          <el-icon><List /></el-icon>
          <span>订单列表</span>
        </template>
        <el-menu-item index="/adminorder_list">
          <el-icon><List /></el-icon>
          <span>订单列表</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/order_refund">
        <el-icon><List /></el-icon>
        <span>售后订单</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/setting_distribution_deliver">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>发货</span>
      </template>
      <el-menu-item index="/setting_distribution_deliver">
        <el-icon><Setting /></el-icon>
        <span>发货设置</span>
      </el-menu-item>
      <el-menu-item index="/setting_freight_shipping_templates_list">
        <el-icon><Menu /></el-icon>
        <span>运费模板</span>
      </el-menu-item>
      <el-menu-item index="/setting_freight_express_index">
        <el-icon><Menu /></el-icon>
        <span>物流公司</span>
      </el-menu-item>
      <el-menu-item index="/setting_delivery_service_index">
        <el-icon><Menu /></el-icon>
        <span>配送员管理</span>
      </el-menu-item>
      <el-menu-item index="/setting_shop_storeList">
        <el-icon><Menu /></el-icon>
        <span>自提点列表</span>
      </el-menu-item>
      <el-menu-item index="/setting_city_delivery_setting">
        <el-icon><Setting /></el-icon>
        <span>配送设置</span>
      </el-menu-item>
      <el-menu-item index="/setting_city_delivery_record">
        <el-icon><Menu /></el-icon>
        <span>配送记录</span>
      </el-menu-item>
      <el-menu-item index="/setting_freight_city_list">
        <el-icon><Menu /></el-icon>
        <span>城市数据</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/setting_shop">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>商城设置</span>
      </template>
      <el-menu-item index="/setting_shop_product">
        <el-icon><Goods /></el-icon>
        <span>商品设置</span>
      </el-menu-item>
      <el-menu-item index="/setting_shop_trade">
        <el-icon><Setting /></el-icon>
        <span>交易设置</span>
      </el-menu-item>
      <el-menu-item index="/setting_shop_agreemant">
        <el-icon><Menu /></el-icon>
        <span>政策协议</span>
      </el-menu-item>
      <el-menu-item index="/setting_shop_releaseset">
        <el-icon><Setting /></el-icon>
        <span>释放比例设置</span>
      </el-menu-item>
      <el-menu-item index="/setting_shop_coinoffset">
        <el-icon><Setting /></el-icon>
        <span>屏蔽前端代币设置</span>
      </el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/user">
    <template #title>
      <el-icon><User /></el-icon>
      <span>用户</span>
    </template>
    <el-menu-item index="/statistic_user">
      <el-icon><User /></el-icon>
      <span>用户概况</span>
    </el-menu-item>
    <el-sub-menu index="/user_manage">
      <template #title>
        <el-icon><User /></el-icon>
        <span>用户</span>
      </template>
      <el-menu-item index="/user_list">
        <el-icon><User /></el-icon>
        <span>用户列表</span>
      </el-menu-item>
      <el-menu-item index="/user_group">
        <el-icon><User /></el-icon>
        <span>用户分组</span>
      </el-menu-item>
      <el-sub-menu index="/user_label">
        <template #title>
          <el-icon><User /></el-icon>
          <span>用户标签</span>
        </template>
        <el-menu-item index="/user_label_create">
          <el-icon><Menu /></el-icon>
          <span>添加标签</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/marketing_channel_code">
        <template #title>
          <el-icon><Connection /></el-icon>
          <span>渠道码</span>
        </template>
        <el-menu-item index="/marketing_channel_code_create">
          <el-icon><Connection /></el-icon>
          <span>添加渠道码</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/user_userSet">
        <el-icon><User /></el-icon>
        <span>用户设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/user">
      <template #title>
        <el-icon><User /></el-icon>
        <span>用户运营</span>
      </template>
      <el-menu-item index="/vipuser_level_list">
        <el-icon><User /></el-icon>
        <span>用户等级</span>
      </el-menu-item>
      <el-menu-item index="/user_levelSet">
        <el-icon><Setting /></el-icon>
        <span>等级设置</span>
      </el-menu-item>
      <el-menu-item index="/user_registerSet">
        <el-icon><Menu /></el-icon>
        <span>新人礼包</span>
      </el-menu-item>
      <el-menu-item index="/user_memberGift">
        <el-icon><Menu /></el-icon>
        <span>激活有礼</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_store_coupon">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>优惠券</span>
      </template>
      <el-sub-menu index="/marketing_store_coupon_issue_index">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>优惠券列表</span>
        </template>
        <el-menu-item index="/marketing_store_coupon_issue_create">
          <el-icon><Menu /></el-icon>
          <span>添加优惠卷</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/marketing_store_coupon_user_index">
        <el-icon><Menu /></el-icon>
        <span>领取记录</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_integral_system_config_3_11">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>资产</span>
      </template>
      <el-menu-item index="/marketing_integral_system_config">
        <el-icon><Setting /></el-icon>
        <span>积分配置</span>
      </el-menu-item>
      <el-menu-item index="/marketing_user_point_index">
        <el-icon><Menu /></el-icon>
        <span>积分日志</span>
      </el-menu-item>
      <el-menu-item index="/marketing_balance_recharge">
        <el-icon><Menu /></el-icon>
        <span>代币金额</span>
      </el-menu-item>
      <el-menu-item index="/integral_release_index">
        <el-icon><Setting /></el-icon>
        <span>积分释放配置</span>
      </el-menu-item>
      <el-menu-item index="/marketing_weather_tpapply">
        <el-icon><Menu /></el-icon>
        <span>代币审核列表</span>
      </el-menu-item>
      <el-menu-item index="/marketing_weather_tongpiao">
        <el-icon><User /></el-icon>
        <span>用户账单</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/work">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>企业微信</span>
      </template>
      <el-sub-menu index="/work_client_list">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>客户管理</span>
        </template>
        <el-menu-item index="/work_channel_code">
          <el-icon><Connection /></el-icon>
          <span>企微渠道码</span>
        </el-menu-item>
        <el-menu-item index="/work_welcome">
          <el-icon><Menu /></el-icon>
          <span>欢迎语</span>
        </el-menu-item>
        <el-menu-item index="/work_createCode">
          <el-icon><Connection /></el-icon>
          <span>添加企业渠道码</span>
        </el-menu-item>
        <el-menu-item index="/work_addWelcome">
          <el-icon><Menu /></el-icon>
          <span>新建好友欢迎语</span>
        </el-menu-item>
        <el-menu-item index="/work_client_list">
          <el-icon><Menu /></el-icon>
          <span>客户列表</span>
        </el-menu-item>
        <el-menu-item index="/work_client_group">
          <el-icon><Menu /></el-icon>
          <span>客户群发</span>
        </el-menu-item>
        <el-menu-item index="/work_client_add_group">
          <el-icon><Menu /></el-icon>
          <span>添加客户群发</span>
        </el-menu-item>
        <el-menu-item index="/work_client_add_moment">
          <el-icon><Menu /></el-icon>
          <span>朋友圈添加</span>
        </el-menu-item>
        <el-menu-item index="/work_client_moment">
          <el-icon><Menu /></el-icon>
          <span>朋友圈列表</span>
        </el-menu-item>
        <el-menu-item index="/work_client_group_info">
          <el-icon><Menu /></el-icon>
          <span>客户群发详情</span>
        </el-menu-item>
        <el-menu-item index="/work_client_moment_info">
          <el-icon><Menu /></el-icon>
          <span>朋友圈详情</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/work_client_group_chat">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>客户群运营</span>
        </template>
        <el-menu-item index="/work_client_group_chat">
          <el-icon><Menu /></el-icon>
          <span>客户群列表</span>
        </el-menu-item>
        <el-menu-item index="/work_auth_group">
          <el-icon><Menu /></el-icon>
          <span>自动拉群</span>
        </el-menu-item>
        <el-menu-item index="/work_addAuthGroup">
          <el-icon><Menu /></el-icon>
          <span>新建自动拉群</span>
        </el-menu-item>
        <el-menu-item index="/work_client_statistical">
          <el-icon><DataAnalysis /></el-icon>
          <span>客户群统计</span>
        </el-menu-item>
        <el-menu-item index="/work_group_template">
          <el-icon><Menu /></el-icon>
          <span>客户群群发</span>
        </el-menu-item>
        <el-menu-item index="/work_group_add_template">
          <el-icon><Menu /></el-icon>
          <span>添加客户群群发</span>
        </el-menu-item>
        <el-menu-item index="/work_group_template_info">
          <el-icon><Menu /></el-icon>
          <span>客户群群发详情</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/work_staffList">
        <el-icon><Menu /></el-icon>
        <span>员工列表</span>
      </el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/user_importRecord">
      <el-icon><User /></el-icon>
      <span>用户导入记录</span>
    </el-menu-item>
  </el-sub-menu>
  <el-sub-menu index="/marketing">
    <template #title>
      <el-icon><Present /></el-icon>
      <span>营销</span>
    </template>
    <el-menu-item index="/marketing_home">
      <el-icon><Present /></el-icon>
      <span>营销中心</span>
    </el-menu-item>
    <el-sub-menu index="/vipuser_grade">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>付费会员</span>
      </template>
      <el-menu-item index="/vipuser_grade_type">
        <el-icon><Menu /></el-icon>
        <span>会员类型</span>
      </el-menu-item>
      <el-menu-item index="/vipuser_grade_right">
        <el-icon><Menu /></el-icon>
        <span>会员权益</span>
      </el-menu-item>
      <el-menu-item index="/vipuser_grade_agreement">
        <el-icon><Menu /></el-icon>
        <span>会员协议</span>
      </el-menu-item>
      <el-menu-item index="/vipuser_grade_card">
        <el-icon><Menu /></el-icon>
        <span>卡密会员</span>
      </el-menu-item>
      <el-menu-item index="/vipuser_grade_record">
        <el-icon><Menu /></el-icon>
        <span>会员记录</span>
      </el-menu-item>
      <el-menu-item index="/vipuser_grade_list">
        <el-icon><Menu /></el-icon>
        <span>会员卡列表</span>
      </el-menu-item>
      <el-menu-item index="/user_svipSet">
        <el-icon><Setting /></el-icon>
        <span>会员设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_lottery_index">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>抽奖</span>
      </template>
      <el-sub-menu index="/marketing_lottery_list">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>抽奖列表</span>
        </template>
        <el-menu-item index="/marketing_lottery_create">
          <el-icon><Setting /></el-icon>
          <span>抽奖配置</span>
        </el-menu-item>
        <el-menu-item index="/marketing_lottery_recording_list">
          <el-icon><Menu /></el-icon>
          <span>中奖记录</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/marketing_lottery_config">
        <el-icon><Setting /></el-icon>
        <span>抽奖配置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_store_combination">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>拼团</span>
      </template>
      <el-menu-item index="/marketing_store_combination_index">
        <el-icon><Goods /></el-icon>
        <span>拼团商品</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_combination_combina_list">
        <el-icon><Menu /></el-icon>
        <span>拼团列表</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_combination_create">
        <el-icon><Menu /></el-icon>
        <span>添加拼团</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_combination_statistics">
        <el-icon><DataAnalysis /></el-icon>
        <span>拼团统计</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_store_seckill">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>秒杀</span>
      </template>
      <el-menu-item index="/marketing_store_seckill_list">
        <el-icon><Menu /></el-icon>
        <span>秒杀列表</span>
      </el-menu-item>
      <el-sub-menu index="/marketing_store_seckill_index">
        <template #title>
          <el-icon><Goods /></el-icon>
          <span>秒杀商品</span>
        </template>
        <el-menu-item index="/marketing_store_seckill_statistics">
          <el-icon><DataAnalysis /></el-icon>
          <span>秒杀统计</span>
        </el-menu-item>
        <el-menu-item index="/marketing_store_seckill_create">
          <el-icon><Menu /></el-icon>
          <span>添加秒杀</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/marketing_store_seckill_data_index">
        <el-icon><Setting /></el-icon>
        <span>秒杀配置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_store_bargain">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>砍价</span>
      </template>
      <el-menu-item index="/marketing_store_bargain_index">
        <el-icon><Goods /></el-icon>
        <span>砍价商品</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_bargain_create">
        <el-icon><Menu /></el-icon>
        <span>添加砍价</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_bargain_bargain_list">
        <el-icon><Menu /></el-icon>
        <span>砍价列表</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_bargain_setting">
        <el-icon><Setting /></el-icon>
        <span>砍价设置</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_bargain_statistics">
        <el-icon><DataAnalysis /></el-icon>
        <span>砍价统计</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_giftCard">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>礼品卡</span>
      </template>
      <el-menu-item index="/marketing_giftCard_manage">
        <el-icon><Menu /></el-icon>
        <span>生成卡号</span>
      </el-menu-item>
      <el-menu-item index="/marketing_giftCard_index">
        <el-icon><Menu /></el-icon>
        <span>礼品卡列表</span>
      </el-menu-item>
      <el-menu-item index="/marketing_giftCard_record">
        <el-icon><Menu /></el-icon>
        <span>卡密管理</span>
      </el-menu-item>
      <el-menu-item index="/marketing_giftCard_create">
        <el-icon><Menu /></el-icon>
        <span>添加礼品卡</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/sysytem_automation">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>自动化运营</span>
      </template>
      <el-menu-item index="/marketing_automation">
        <el-icon><Menu /></el-icon>
        <span>智能推送</span>
      </el-menu-item>
      <el-menu-item index="/marketing_automation_create">
        <el-icon><Menu /></el-icon>
        <span>创建定时任务</span>
      </el-menu-item>
      <el-menu-item index="/marketing_birthday">
        <el-icon><Menu /></el-icon>
        <span>生日有礼</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_discount">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>促销</span>
      </template>
      <el-sub-menu index="/marketing_discount_list">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>限时折扣</span>
        </template>
        <el-menu-item index="/marketing_discount_add">
          <el-icon><Menu /></el-icon>
          <span>添加限时折扣</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/marketing_discount_full_discount">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>满减满折</span>
        </template>
        <el-menu-item index="/marketing_discount_add_discount">
          <el-icon><Menu /></el-icon>
          <span>添加满减满折</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/marketing_discount_give">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>满送活动</span>
        </template>
        <el-menu-item index="/marketing_discount_add_give">
          <el-icon><Menu /></el-icon>
          <span>添加满减送</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/marketing_discount_pieces_discount">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>第N件N折</span>
        </template>
        <el-menu-item index="/marketing_discount_add_pieces">
          <el-icon><Menu /></el-icon>
          <span>添加第N件N折</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/marketing_store_discounts_index">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>组合套餐</span>
        </template>
        <el-menu-item index="/marketing_store_discounts_create">
          <el-icon><Menu /></el-icon>
          <span>添加、编辑优惠套餐</span>
        </el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-sub-menu index="/marketing_user_point">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>积分</span>
      </template>
      <el-menu-item index="/marketing_integral_classify">
        <el-icon><Menu /></el-icon>
        <span>积分分类</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_integral_index">
        <el-icon><Goods /></el-icon>
        <span>积分商品</span>
      </el-menu-item>
      <el-menu-item index="/marketing_store_integral_create">
        <el-icon><Goods /></el-icon>
        <span>添加积分商品</span>
      </el-menu-item>
      <el-menu-item index="/pages_marketing_store_integral_add_store_integral">
        <el-icon><Goods /></el-icon>
        <span>批量添加积分商品</span>
      </el-menu-item>
      <el-menu-item index="/marketing_point_statistic">
        <el-icon><DataAnalysis /></el-icon>
        <span>积分统计</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_sign">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>签到</span>
      </template>
      <el-menu-item index="/marketing_sign_config">
        <el-icon><Setting /></el-icon>
        <span>签到配置</span>
      </el-menu-item>
      <el-menu-item index="/marketing_sign_rewards">
        <el-icon><Menu /></el-icon>
        <span>签到奖励</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/marketing_activity_background">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>活动氛围</span>
      </template>
      <el-sub-menu index="/marketing_activity_frame">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>活动边框</span>
        </template>
        <el-menu-item index="/marketing_activity_frame_create">
          <el-icon><Menu /></el-icon>
          <span>添加活动边框</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/marketing_activity_background">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>活动背景</span>
        </template>
        <el-menu-item index="/marketing_activity_background_create">
          <el-icon><Menu /></el-icon>
          <span>添加活动背景</span>
        </el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/agent">
    <template #title>
      <el-icon><Share /></el-icon>
      <span>分销</span>
    </template>
    <el-sub-menu index="/agent_agent_manage_index">
      <template #title>
        <el-icon><Share /></el-icon>
        <span>分销员</span>
      </template>
      <el-menu-item index="/agent_agent_manage_index">
        <el-icon><Share /></el-icon>
        <span>分销员管理</span>
      </el-menu-item>
      <el-menu-item index="/setting_membership_level_index">
        <el-icon><Share /></el-icon>
        <span>分销员等级</span>
      </el-menu-item>
      <el-menu-item index="/finance_finance_commission">
        <el-icon><Menu /></el-icon>
        <span>佣金记录</span>
      </el-menu-item>
      <el-menu-item index="/agent_promoter_apply">
        <el-icon><Share /></el-icon>
        <span>分销员申请</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/setting_system_config_retail_2_9">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>分销配置</span>
      </template>
      <el-menu-item index="/setting_system_config_retail_2_9">
        <el-icon><Share /></el-icon>
        <span>分销模式</span>
      </el-menu-item>
      <el-menu-item index="/setting_system_config_rake_back">
        <el-icon><Setting /></el-icon>
        <span>返佣设置</span>
      </el-menu-item>
      <el-menu-item index="/agent_agreement">
        <el-icon><Share /></el-icon>
        <span>分销说明</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/agent_division">
      <template #title>
        <el-icon><Share /></el-icon>
        <span>团队分销</span>
      </template>
      <el-menu-item index="/agent_division_list">
        <el-icon><Menu /></el-icon>
        <span>团队列表</span>
      </el-menu-item>
      <el-menu-item index="/agent_agent_list">
        <el-icon><Menu /></el-icon>
        <span>代理列表</span>
      </el-menu-item>
      <el-menu-item index="/agent_apply_list">
        <el-icon><Menu /></el-icon>
        <span>代理申请</span>
      </el-menu-item>
      <el-menu-item index="/setting_shop_division">
        <el-icon><Setting /></el-icon>
        <span>团队配置</span>
      </el-menu-item>
      <el-menu-item index="/agent_statistics">
        <el-icon><DataAnalysis /></el-icon>
        <span>团队统计</span>
      </el-menu-item>
      <el-menu-item index="/agent_order">
        <el-icon><List /></el-icon>
        <span>团队订单</span>
      </el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/setting_pages">
    <template #title>
      <el-icon><Shop /></el-icon>
      <span>店铺</span>
    </template>
    <el-sub-menu index="/setting_pages">
      <template #title>
        <el-icon><Shop /></el-icon>
        <span>店铺装修</span>
      </template>
      <el-menu-item index="/setting_pages_devise">
        <el-icon><Menu /></el-icon>
        <span>首页装修</span>
      </el-menu-item>
      <el-menu-item index="/setting_theme_style">
        <el-icon><Menu /></el-icon>
        <span>主题风格</span>
      </el-menu-item>
      <el-menu-item index="/setting_pages_product_category">
        <el-icon><Goods /></el-icon>
        <span>商品分类</span>
      </el-menu-item>
      <el-menu-item index="/setting_pages_home">
        <el-icon><Menu /></el-icon>
        <span>个人中心</span>
      </el-menu-item>
      <el-menu-item index="/setting_pages_product_detail">
        <el-icon><Goods /></el-icon>
        <span>商品详情</span>
      </el-menu-item>
      <el-menu-item index="/setting_pages_fab">
        <el-icon><Menu /></el-icon>
        <span>悬浮菜单</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/system_file">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>通用组件</span>
      </template>
      <el-menu-item index="/setting_system_visualization_data">
        <el-icon><Menu /></el-icon>
        <span>开屏广告</span>
      </el-menu-item>
      <el-menu-item index="/product_hotWords">
        <el-icon><Menu /></el-icon>
        <span>搜索热词</span>
      </el-menu-item>
      <el-menu-item index="/system_file">
        <el-icon><Menu /></el-icon>
        <span>素材中心</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/content_community">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>逛逛社区</span>
      </template>
      <el-menu-item index="/content_community_topic">
        <el-icon><Menu /></el-icon>
        <span>社区话题</span>
      </el-menu-item>
      <el-sub-menu index="/content_community_content">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>社区内容</span>
        </template>
        <el-menu-item index="/content_community_addContent">
          <el-icon><Menu /></el-icon>
          <span>添加社区内容</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/content_community_comment">
        <el-icon><Menu /></el-icon>
        <span>社区评论</span>
      </el-menu-item>
      <el-menu-item index="/content_community_setting">
        <el-icon><Setting /></el-icon>
        <span>社区设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/content_cms">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>内容资讯</span>
      </template>
      <el-menu-item index="/content_article_category_index">
        <el-icon><Document /></el-icon>
        <span>文章分类</span>
      </el-menu-item>
      <el-menu-item index="/content_article_index">
        <el-icon><Document /></el-icon>
        <span>文章列表</span>
      </el-menu-item>
      <el-menu-item index="/content_article_add_article">
        <el-icon><Document /></el-icon>
        <span>文章添加</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/kefu">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>客服管理</span>
      </template>
      <el-menu-item index="/setting_store_service_index">
        <el-icon><Menu /></el-icon>
        <span>客服列表</span>
      </el-menu-item>
      <el-menu-item index="/setting_store_service_speechcraft">
        <el-icon><Menu /></el-icon>
        <span>客服话术</span>
      </el-menu-item>
      <el-menu-item index="/setting_store_service_feedback">
        <el-icon><User /></el-icon>
        <span>用户留言</span>
      </el-menu-item>
      <el-menu-item index="/kefu_setup">
        <el-icon><Setting /></el-icon>
        <span>客服设置</span>
      </el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/admin_supplier">
    <template #title>
      <el-icon><Connection /></el-icon>
      <span>渠道</span>
    </template>
    <el-sub-menu index="/supplier">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>供应商</span>
      </template>
      <el-menu-item index="/supplier_menu_list">
        <el-icon><Menu /></el-icon>
        <span>供应商列表</span>
      </el-menu-item>
      <el-menu-item index="/supplier_apply">
        <el-icon><Menu /></el-icon>
        <span>供应商申请</span>
      </el-menu-item>
      <el-menu-item index="/supplier_orderList_index">
        <el-icon><List /></el-icon>
        <span>订单列表</span>
      </el-menu-item>
      <el-menu-item index="/supplier_afterOrder_index">
        <el-icon><List /></el-icon>
        <span>售后订单</span>
      </el-menu-item>
      <el-menu-item index="/supplier_orderStatistics_index">
        <el-icon><List /></el-icon>
        <span>订单统计</span>
      </el-menu-item>
      <el-menu-item index="/supplier_supplier_index">
        <el-icon><Setting /></el-icon>
        <span>菜单设置</span>
      </el-menu-item>
      <el-menu-item index="/supplier_supplierAdd">
        <el-icon><Menu /></el-icon>
        <span>添加供应商</span>
      </el-menu-item>
      <el-menu-item index="/supplier_setting">
        <el-icon><Setting /></el-icon>
        <span>供应商设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/user_channelMerchant">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>采购商</span>
      </template>
      <el-menu-item index="/user_channelMerchant_examine">
        <el-icon><Menu /></el-icon>
        <span>采购商审核</span>
      </el-menu-item>
      <el-menu-item index="/user_channelMerchant_list">
        <el-icon><Menu /></el-icon>
        <span>采购商列表</span>
      </el-menu-item>
      <el-menu-item index="/user_channelMerchant_identity">
        <el-icon><Menu /></el-icon>
        <span>采购商身份</span>
      </el-menu-item>
      <el-menu-item index="/user_channelMerchant_setting">
        <el-icon><Setting /></el-icon>
        <span>采购商设置</span>
      </el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/finance">
    <template #title>
      <el-icon><Money /></el-icon>
      <span>财务</span>
    </template>
    <el-sub-menu index="/finance_user_extract">
      <template #title>
        <el-icon><Money /></el-icon>
        <span>财务操作</span>
      </template>
      <el-menu-item index="/order_invoice_list">
        <el-icon><Menu /></el-icon>
        <span>发票列表</span>
      </el-menu-item>
      <el-menu-item index="/order_invoice_setup">
        <el-icon><Setting /></el-icon>
        <span>发票设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/finance_user_extract_index">
      <template #title>
        <el-icon><Share /></el-icon>
        <span>分销财务</span>
      </template>
      <el-menu-item index="/finance_user_extract_index">
        <el-icon><Menu /></el-icon>
        <span>提现申请</span>
      </el-menu-item>
      <el-menu-item index="/setting_system_config_advance">
        <el-icon><Setting /></el-icon>
        <span>提现设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/supplier_finance">
      <template #title>
        <el-icon><Money /></el-icon>
        <span>供应商财务</span>
      </template>
      <el-menu-item index="/supplier_capital_index">
        <el-icon><Money /></el-icon>
        <span>资金流水</span>
      </el-menu-item>
      <el-menu-item index="/supplier_bill_index">
        <el-icon><Menu /></el-icon>
        <span>账单记录</span>
      </el-menu-item>
      <el-menu-item index="/supplier_cash_index">
        <el-icon><Menu /></el-icon>
        <span>转账申请</span>
      </el-menu-item>
      <el-menu-item index="/supplier_bill_index_1">
        <el-icon><Menu /></el-icon>
        <span>对账管理</span>
      </el-menu-item>
      <el-menu-item index="/supplier_finance_set">
        <el-icon><Setting /></el-icon>
        <span>财务设置</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/finance_user_recharge">
      <template #title>
        <el-icon><Money /></el-icon>
        <span>财务记录</span>
      </template>
      <el-menu-item index="/finance_user_recharge_index">
        <el-icon><Menu /></el-icon>
        <span>充值记录</span>
      </el-menu-item>
      <el-menu-item index="/statistic_capital">
        <el-icon><Money /></el-icon>
        <span>资金流水</span>
      </el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  <el-menu-item index="/statistic">
    <el-icon><DataAnalysis /></el-icon>
    <span>统计</span>
  </el-menu-item>
  <el-sub-menu index="/app">
    <template #title>
      <el-icon><Monitor /></el-icon>
      <span>应用端</span>
    </template>
    <el-sub-menu index="/app_wechat">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>公众号</span>
      </template>
      <el-menu-item index="/app_wechat_base">
        <el-icon><Setting /></el-icon>
        <span>基础配置</span>
      </el-menu-item>
      <el-menu-item index="/app_wechat_setting_menus_index">
        <el-icon><Menu /></el-icon>
        <span>微信菜单</span>
      </el-menu-item>
      <el-menu-item index="/app_wechat_card">
        <el-icon><Menu /></el-icon>
        <span>微信会员卡</span>
      </el-menu-item>
      <el-menu-item index="/app_wechat_reply">
        <el-icon><Menu /></el-icon>
        <span>自动回复</span>
      </el-menu-item>
      <el-sub-menu index="/app_wechat_news_category_index">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>图文管理</span>
        </template>
        <el-menu-item index="/app_wechat_news_category_save">
          <el-icon><Menu /></el-icon>
          <span>图文添加</span>
        </el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-sub-menu index="/app_routine_download">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>小程序</span>
      </template>
      <el-menu-item index="/app_routine_download">
        <el-icon><Setting /></el-icon>
        <span>小程序配置</span>
      </el-menu-item>
      <el-sub-menu index="/content_live_live_room">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>直播间管理</span>
        </template>
        <el-menu-item index="/content_live_add_live_room">
          <el-icon><Menu /></el-icon>
          <span>添加直播间</span>
        </el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="/content_live_live_goods">
        <template #title>
          <el-icon><Goods /></el-icon>
          <span>商品管理</span>
        </template>
        <el-menu-item index="/content_live_add_live_goods">
          <el-icon><Goods /></el-icon>
          <span>添加直播商品</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/content_live_anchor">
        <el-icon><Menu /></el-icon>
        <span>主播管理</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/app_pc">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>PC 端</span>
      </template>
      <el-menu-item index="/app_pc">
        <el-icon><Setting /></el-icon>
        <span>PC 配置</span>
      </el-menu-item>
      <el-menu-item index="/setting_pc_group_data">
        <el-icon><Menu /></el-icon>
        <span>PC商城</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/work_config">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>企业微信</span>
      </template>
      <el-menu-item index="/work_config">
        <el-icon><Setting /></el-icon>
        <span>企微设置</span>
      </el-menu-item>
    </el-sub-menu>
  </el-sub-menu>
  <el-sub-menu index="/setting">
    <template #title>
      <el-icon><Setting /></el-icon>
      <span>设置</span>
    </template>
    <el-sub-menu index="/setting_base">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>系统设置</span>
      </template>
      <el-menu-item index="/setting_shop_base">
        <el-icon><Setting /></el-icon>
        <span>系统设置</span>
      </el-menu-item>
      <el-sub-menu index="/setting_notification_index">
        <template #title>
          <el-icon><Setting /></el-icon>
          <span>消息设置</span>
        </template>
        <el-menu-item index="/setting_notification_notificationEdit">
          <el-icon><Setting /></el-icon>
          <span>消息设置</span>
        </el-menu-item>
      </el-sub-menu>
    </el-sub-menu>
    <el-sub-menu index="/setting_service">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>服务设置</span>
      </template>
      <el-menu-item index="/setting_sms_sms_config_index">
        <el-icon><Menu /></el-icon>
        <span>一号通管理</span>
      </el-menu-item>
      <el-menu-item index="/setting_system_config_sms">
        <el-icon><Setting /></el-icon>
        <span>一号通配置</span>
      </el-menu-item>
      <el-menu-item index="/setting_third_party">
        <el-icon><Setting /></el-icon>
        <span>接口设置</span>
      </el-menu-item>
      <el-menu-item index="/setting_document">
        <el-icon><Menu /></el-icon>
        <span>小票打印</span>
      </el-menu-item>
      <el-menu-item index="/setting_shop_pay">
        <el-icon><Setting /></el-icon>
        <span>支付设置</span>
      </el-menu-item>
      <el-menu-item index="/setting_storage">
        <el-icon><Setting /></el-icon>
        <span>存储配置</span>
      </el-menu-item>
      <el-menu-item index="/setting_document_content">
        <el-icon><Menu /></el-icon>
        <span>小票打印</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/setting_auth_list">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>权限设置</span>
      </template>
      <el-menu-item index="/setting_system_role_index">
        <el-icon><Menu /></el-icon>
        <span>角色管理</span>
      </el-menu-item>
      <el-menu-item index="/setting_system_admin_index">
        <el-icon><Menu /></el-icon>
        <span>管理员列表</span>
      </el-menu-item>
      <el-menu-item index="/setting_system_menus_index">
        <el-icon><Menu /></el-icon>
        <span>权限规则</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/system_config">
      <template #title>
        <el-icon><Setting /></el-icon>
        <span>开发配置</span>
      </template>
      <el-sub-menu index="/system_crontab">
        <template #title>
          <el-icon><Menu /></el-icon>
          <span>定时任务</span>
        </template>
        <el-menu-item index="/system_crontab_create">
          <el-icon><Menu /></el-icon>
          <span>添加定时任务</span>
        </el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/system_config_system_config_tab_index">
        <el-icon><Setting /></el-icon>
        <span>配置分类</span>
      </el-menu-item>
      <el-menu-item index="/system_config_system_group_index">
        <el-icon><Menu /></el-icon>
        <span>组合数据</span>
      </el-menu-item>
      <el-menu-item index="/system_config_system_config_tab_list">
        <el-icon><Setting /></el-icon>
        <span>配置列表</span>
      </el-menu-item>
      <el-menu-item index="/system_config_system_group_list">
        <el-icon><Menu /></el-icon>
        <span>组合数据列表</span>
      </el-menu-item>
      <el-menu-item index="/out">
        <el-icon><Menu /></el-icon>
        <span>对外接口</span>
      </el-menu-item>
      <el-menu-item index="/out_interface">
        <el-icon><Menu /></el-icon>
        <span>接口文档</span>
      </el-menu-item>
    </el-sub-menu>
    <el-sub-menu index="/system_maintain">
      <template #title>
        <el-icon><Menu /></el-icon>
        <span>安全维护</span>
      </template>
      <el-menu-item index="/system_maintain_clear_index">
        <el-icon><Menu /></el-icon>
        <span>刷新缓存</span>
      </el-menu-item>
      <el-menu-item index="/system_maintain_system_log_index">
        <el-icon><Menu /></el-icon>
        <span>系统日志</span>
      </el-menu-item>
      <el-menu-item index="/system_maintain_system_file_index">
        <el-icon><Menu /></el-icon>
        <span>文件校验</span>
      </el-menu-item>
      <el-menu-item index="/system_maintain_system_cleardata_index">
        <el-icon><Menu /></el-icon>
        <span>清除数据</span>
      </el-menu-item>
      <el-menu-item index="/system_maintain_system_databackup_index">
        <el-icon><Menu /></el-icon>
        <span>数据备份</span>
      </el-menu-item>
      <el-menu-item index="/system_log">
        <el-icon><Menu /></el-icon>
        <span>系统日志</span>
      </el-menu-item>
    </el-sub-menu>
    <el-menu-item index="/system_user">
      <el-icon><Menu /></el-icon>
      <span>个人中心</span>
    </el-menu-item>
  </el-sub-menu>
</el-menu>
    </el-aside>

    <!-- Main Content -->
    <el-container class="main-container">
      <!-- Header -->
      <el-header class="header" height="60px">
        <div class="header-left">
          <el-icon class="collapse-icon" @click="toggleCollapse">
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">主页</el-breadcrumb-item>
            <el-breadcrumb-item v-if="currentRouteName !== 'Home'">{{ currentRouteName }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <div class="header-actions">
            <el-icon class="action-icon" @click="toggleTheme" title="切换到新版UI"><SwitchButton /></el-icon>
            <el-icon class="action-icon"><Search /></el-icon>
            <el-icon class="action-icon"><Bell /></el-icon>
            <el-icon class="action-icon"><FullScreen /></el-icon>
          </div>
          <el-dropdown @command="handleCommand" trigger="click">
            <span class="el-dropdown-link userinfo">
              <el-avatar size="small" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"></el-avatar>
              <span class="username">Admin</span>
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- Tags View (Placeholder) -->
      <div class="tags-view-container">
        <div class="tags-view-item active">
          {{ currentRouteName === 'Home' ? '主页' : currentRouteName }}
        </div>
      </div>

      <!-- Content -->
      <el-main class="content">
        <div class="content-wrapper">
          <router-view v-slot="{ Component }">
            <transition name="fade-transform" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu, Fold, Expand, ArrowDown, Setting, User, Goods, List, Money, DataLine, Search, Bell, FullScreen, ChatLineRound, Present, Document, Share, DataAnalysis, Shop, Connection, Monitor, ChatDotRound, SwitchButton } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const isCollapse = ref(false)

const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

const currentRouteName = computed(() => {
  return route.name
})

const toggleTheme = () => {
  localStorage.setItem('ui_theme', 'v2')
  window.location.reload()
}

const handleCommand = (command) => {
  if (command === 'logout') {
    localStorage.removeItem('admin_token')
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  width: 100vw;
}

.sidebar {
  background-color: #001529;
  color: white;
  transition: width 0.2s;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #002140;
  padding: 10px;
  overflow: hidden;
}

.logo-full {
  height: 30px;
}

.logo-mini {
  height: 30px;
  width: 30px;
  object-fit: contain;
}

.el-menu-vertical {
  border-right: none;
  flex: 1;
  overflow-y: auto;
}
/* Custom scrollbar for sidebar */
.el-menu-vertical::-webkit-scrollbar {
  width: 6px;
}
.el-menu-vertical::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.2);
  border-radius: 3px;
}

:deep(.el-menu-item.is-active) {
  background-color: #1890ff !important;
}
:deep(.el-sub-menu__title:hover), :deep(.el-menu-item:hover) {
  background-color: rgba(24,144,255,0.1) !important;
}

.main-container {
  display: flex;
  flex-direction: column;
  background-color: #f0f2f5;
}

.header {
  background-color: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
}

.collapse-icon {
  font-size: 20px;
  cursor: pointer;
  margin-right: 20px;
  color: #5c5c5c;
  transition: color 0.3s;
}
.collapse-icon:hover {
  color: #1890ff;
}

.header-right {
  display: flex;
  align-items: center;
}

.header-actions {
  display: flex;
  align-items: center;
  margin-right: 20px;
}

.action-icon {
  font-size: 18px;
  color: #5c5c5c;
  margin: 0 10px;
  cursor: pointer;
}
.action-icon:hover {
  color: #1890ff;
}

.userinfo {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 0 10px;
}

.username {
  margin-left: 8px;
  font-size: 14px;
  color: #333;
}

.tags-view-container {
  height: 34px;
  width: 100%;
  background: #fff;
  border-bottom: 1px solid #d8dce5;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, .12), 0 0 3px 0 rgba(0, 0, 0, .04);
  display: flex;
  align-items: center;
  padding: 0 15px;
}

.tags-view-item {
  display: inline-block;
  position: relative;
  cursor: pointer;
  height: 26px;
  line-height: 26px;
  border: 1px solid #d8dce5;
  color: #495060;
  background: #fff;
  padding: 0 8px;
  font-size: 12px;
  margin-left: 5px;
  border-radius: 2px;
}
.tags-view-item.active {
  background-color: #1890ff;
  color: #fff;
  border-color: #1890ff;
}

.content {
  padding: 20px;
  overflow-y: auto;
}

.content-wrapper {
  background-color: #fff;
  min-height: calc(100vh - 134px);
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* Page Transition */
.fade-transform-leave-active,
.fade-transform-enter-active {
  transition: all .3s;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
