import streamlit as st
import pandas as pd
import plotly.express as px
import io

# 1. UI Configuration
st.set_page_config(page_title="M&E Project Tracking Dashboard", layout="wide")

# Custom CSS to improve Thai font readability and table styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Sarabun', sans-serif;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. Data Loading & Preprocessing
@st.cache_data
def load_data():
    # In a real scenario, use: df = pd.read_csv('M&E dataset - ชีต1.csv', encoding='utf-8-sig')
    # For this demonstration, I will simulate the loading from the provided text format
    data = """project_code,type,node_name,mentomentor_interviewer,last_data_date,province,project_name_th,node_type,issue_area,budget_thb,project_status,tracker_status,quant_status,qual_status,raw_outcome,data_channel,data_type,references,role_respondents,support_detail,quotation,signal,note,round_dc,quality_notes,action_needed,note_id,age,gender,จำนวนกิจกรรมที่เข้าร่วม,ระดับความรู้ก่อนเข้าร่วม (1–5),ระดับความรู้หลังเข้าร่วม (1–5),การประเมินการเปลี่ยนแปลงพฤติกรรมตนเอง (1–5),มีการนำไปต่อยอด/ทำกิจกรรมต่อหรือไม่,recommendation,fis_year
P-68001,Master,Node พื้นที่ขับเคลื่อนจังหวัด,พี่ตอง,18/4/2026,แพร่,กลไกชุมชนเฝ้าระวังภาวะเปราะบางเด็กและเยาวชน,NT1-AREA,เด็กและเยาวชน,60000,กำลังดำเนินการ,ส่งข้อมูลครบถ้วน,ครบ,มีบันทึกสัมภาษณ์,อสม.มีความรู้ในการคัดกรองเด็กเสี่ยงและเริ่มใช้แบบประเมินในชุมชน,Line group,,proposal.pdf; mentor_note.docx,,,,,,,ข้อมูลเชิงปริมาณมีครบ แต่ยังไม่มีหลักฐานการใช้แบบประเมินจริง,ขอภาพกิจกรรม/ตัวอย่างแบบคัดกรองที่ใช้จริง,1,,,,,,,,,2568
P-68002,Master,Node พลังเด็ก,พี่ต้อม,18/4/2026,แพร่,เยาวชนบ้านห้วยปูลิงสืบสานอาหารท้องถิ่น,NT3-POP,อาหาร/วัฒนธรรม,100000,กำลังดำเนินการ,ส่งข้อมูลครบถ้วน,Complete,มี note,เยาวชนรู้จักพืชผักพื้นบ้านมากขึ้นและชุมชนตื่นตัว,Google Drive,,รูปกิจกรรม 12 รูป,,,,,status ภาษาอังกฤษปนไทย,,ผลลัพธ์เขียนค่อนข้างกว้าง ยังไม่ชัดว่าเปลี่ยนพฤติกรรมหรือแค่เข้าร่วมกิจกรรม,ตามจำนวนเยาวชนที่เข้าร่วมจริงและตัวอย่างกิจกรรมหลังโครงการ,2,,,,,,,,,2568
P-68002,Quantitative,Node พลังเด็ก,พี่ต้อม,10/4/2026,แพร่,เยาวชนบ้านห้วยปูลิงสืบสานอาหารท้องถิ่น,NT3-POP,อาหาร/วัฒนธรรม,100000,,,,,,,,,แกนนำโครงการ,,,,,midline,,,R011,17,หญิง,3,2,4,4,ใช่,รู้จักผักพื้นบ้านและทำกิจกรรมกับผู้สูงอายุ,
P-68002,Quantitative,Node พลังเด็ก,พี่ต้อม,10/4/2026,แพร่,เยาวชนบ้านห้วยปูลิงสืบสานอาหารท้องถิ่น,NT3-POP,อาหาร/วัฒนธรรม,100000,,,,,,,,,กลุ่มเป้าหมาย,,,,missing baseline score,midline,,,R012,16,หญิง,1,,4,3,ไม่ระบุ,ไม่ได้ตอบก่อนเข้าร่วม,
P-68002,Qualitative,Node พลังเด็ก,พี่ต้อม,10/4/2026,แพร่,เยาวชนบ้านห้วยปูลิงสืบสานอาหารท้องถิ่น,NT3-POP,อาหาร/วัฒนธรรม,100000,,,,,เด็ก ๆ สนใจมาก บรรยากาศดีมาก กิจกรรมสนุก ชุมชนชอบ,,บันทึกกิจกรรม,photos.zip,พี่เลี้ยง,ไม่มีรายละเอียดว่าเรียนรู้อะไรหรือเปลี่ยนอย่างไร,ไม่มี,การเรียนรู้ของเยาวชน,บันทึกเน้นบรรยากาศ ไม่ใช่ outcome,,,,Q006,,,,,,,,,
P-68003,Master,Node พื้นที่ขับเคลื่อนจังหวัด,พี่บี,,เชียงใหม่,เวียงขยับเมือง ร่วมออกแบบพื้นที่สาธารณะเชียงดาว,NT1-AREA,เมือง/พลเมือง,100000,ไม่พบข้อมูล,ยังไม่กรอกข้อมูล/ล่าช้า,ยังไม่ส่ง,ยังไม่ส่ง,,Airtable,,มีข้อเสนอโครงการ,,,,,สถานะโครงการว่าง,,ยังไม่มีข้อมูลผลลัพธ์หรือข้อมูลภาคสนาม,ติดตามพี่เลี้ยงก่อนรอบสรุปกลางเดือน,3,,,,,,,,,2568
P-68004,Master,Node ฟื้นฟูระบบนิเวศชุมชน,พี่เมย์,22/4/2026,เชียงใหม่,คนรุ่นใหม่ร่วมดูแลทรัพยากรและสิทธิชุมชน,NT2-ISSUE,ทรัพยากรธรรมชาติ,100000,กำลังดำเนินการ,ส่งข้อมูลแล้วบางส่วน,บางส่วน,มีบันทึกสัมภาษณ์,คนรุ่นใหม่เข้าใจสิทธิชุมชนและทำข้อมูลทรัพยากรท้องถิ่นได้,Line OA,,แผนที่ชุมชน draft,,,,,,,quant มีเฉพาะจำนวนคนเข้าร่วม ยังไม่เห็นก่อน-หลังหรือหลักฐานการใช้ข้อมูล,ขอ checklist เครื่องมือและตัวอย่างแผนที่ฉบับล่าสุด,4,,,,,,,,,2568
P-68005,Master,Node เศรษฐกิจชุมชนฐานราก,พี่แก้ว,24/4/2026,ตาก,เกษตรปลอดสารฟื้นระบบพืชหลากหลาย,NT2-ISSUE,เกษตร/สุขภาพ,60000,กำลังดำเนินการ,ข้อมูลไม่ครบถ้วน,มีตัวเลข,ไม่มี note,ครัวเรือนลดการใช้สารเคมีและปลูกพืชผสมผสานมากขึ้น,Email,,summary.xlsx,,,,,,,มีตัวเลข แต่ไม่มีคำอธิบายวิธีเก็บและฐานก่อนโครงการ,ขอคำอธิบายตัวชี้วัดและจำนวนครัวเรือนทั้งหมด,5,,,,,,,,,2568
P-68006,Master,Node ประชากรเฉพาะบริบท,พี่แนน,25/4/2026,พะเยา,สุขภาวะ 5 ด้านของผู้สูงวัยบ้านดอนแก้ว,NT3-POP,ผู้สูงอายุ/สุขภาพกายใจ,60000,ดำเนินการแล้วเสร็จ,ข้อมูลไม่ครบถ้วน,ครบ,ขาดรายละเอียด,ผู้สูงอายุสุขภาพกายใจดีขึ้น มีการรวมกลุ่มทำกิจกรรมต่อ,Google Drive,,รูปกิจกรรม; ตารางผู้เข้าร่วม,,,,,วันที่เป็นปี พ.ศ./ค.ศ. ปนกัน,,ผลลัพธ์เชิงสุขภาพยังเป็น self-report ไม่มีหลักฐานเปรียบเทียบก่อนหลัง,ขอข้อมูล baseline หรือคำอธิบายกิจกรรมต่อเนื่องหลังจบ,6,,,,,,,,,2568
P-68007,Master,Node เศรษฐกิจชุมชนฐานราก,พี่นุ่น,20/4/2026,แม่ฮ่องสอน,เศรษฐกิจฐานรากพืชเศรษฐกิจบ้านพ่อเสือใต้,NT2-ISSUE,เศรษฐกิจ/อาชีพ,100000,ดำเนินการแล้วเสร็จ,ส่งข้อมูลครบถ้วน,ครบ,มี,เกิดแผนพัฒนากาแฟและกลุ่มแปรรูปเริ่มขายผลิตภัณฑ์,Email,,ยอดขายเดือนแรก; ภาพผลิตภัณฑ์,,,,,คำว่าเสร็จ/เรียบร้อยอาจตีความต่างกัน,,มีข้อมูลเศรษฐกิจเบื้องต้น แต่ไม่ชัดว่าเกิดจากโครงการหรือกิจกรรมเดิมของชุมชน,ขอ timeline ก่อน-หลังและบทบาทของโครงการ,7,,,,,,,,,2568
P-68010,Master,Node พื้นที่ขับเคลื่อนจังหวัด,พี่แหม่ม,12/4/2026,ลำพูน,เกษตรกรคนรุ่นใหม่ปลูกผักปลอดภัยชุมชน,NT1-AREA,เกษตร/อาหาร,100000,กำลังดำเนินการ,ส่งข้อมูลแล้วบางส่วน,บางส่วน,บางส่วน,เกิดความร่วมมือระหว่างกลุ่มเดิมและกลุ่มใหม่,Line group,,รายงานกิจกรรมรอบ 1,,,,,มี inconsistency,,ตัวเลขผู้เข้าร่วมไม่ตรงกันระหว่าง sheet quant กับรายงานกิจกรรม,ขอให้พื้นที่ยืนยันตัวเลขรวมผู้เข้าร่วมและกลุ่มเป้าหมาย,10,,,,,,,,,2568
P-68013,Master,Node ชุมชนเมืองนอกระบบ,พี่แพรว,28/4/2026,กรุงเทพมหานคร,ชุมชนเมืองนอกระบบเข้าถึงสิทธิสุขภาพ กทม.,NT1-AREA,ชุมชนเมือง/สิทธิ,150000,กำลังดำเนินการ,ส่งข้อมูลครบถ้วน,ครบ,มี,ชุมชนที่ตกหล่นเริ่มเข้าถึงช่องทางสนับสนุนและมีแผนสุขภาพชุมชน,Google Drive,,รายงานเวที; แผนชุมชน,,,,,ควรดูเป็น high priority,,เป็นเคสยุทธศาสตร์สำคัญ มีหลักฐานหลายประเภท แต่ต้องตรวจความครบของรายชื่อชุมชน,ขอ list ชุมชนและสถานะการขึ้นทะเบียน/ไม่ขึ้นทะเบียน,13,,,,,,,,,2568
P-68015,Master,แผนงานความร่วมมือท้องถิ่น,พี่ออย,30/4/2026,อุดรธานี,ความร่วมมือท้องถิ่นลดอุปสรรคการเข้าถึงสุขภาพ,WP02-PARTNERSHIP,ร่วมทุน/บริการสุขภาพ,500000,กำลังดำเนินการ,ส่งข้อมูลแล้วบางส่วน,มีตัวเลขบางส่วน,มีสัมภาษณ์,อบจ.และ รพ.สต.ร่วมสนับสนุนกลไกสุขภาพชุมชนต่อเนื่อง,Email,,งบสมทบ อบจ.; interview note,,,,,strategic/economic evaluation candidate,,มีข้อมูลร่วมทุนสำคัญ แต่ตัวเลขผลลัพธ์ด้านบริการยังไม่ครบ,ตามข้อมูล รพ.สต. และหลักฐานงบสมทบ,15,,,,,,,,,2568
P-68016,Master,Node ชุมชนลดเสี่ยงโรคเรื้อรัง,พี่หมิว,29/4/2026,นครราชสีมา,แกนนำสุขภาวะชุมชนลดเสี่ยงโรคไม่ติดต่อ,NT2-ISSUE,NCDs/พฤติกรรมสุขภาพ,180000,ดำเนินการแล้วเสร็จ,ส่งข้อมูลครบถ้วน,ครบ,มี note,แกนนำ 18 คนลดรอบเอวและออกกำลังกายต่อเนื่อง,Google Drive,,body_measurement.xlsx; note,,,,,ดีสำหรับตรวจ data quality,,ข้อมูลเชิงสุขภาพดี แต่ต้องตรวจว่าเป็นคนเดิมก่อน-หลังหรือไม่,cross-check respondent id และวันที่วัดก่อน-หลัง,16,,,,,,,,,2568
"""
    df = pd.read_csv(io.StringIO(data), encoding='utf-8')
    
    # Preprocessing
    df['budget_thb'] = pd.to_numeric(df['budget_thb'], errors='coerce').fillna(0)
    df['project_name_full'] = df['project_code'] + ": " + df['project_name_th']
    
    return df

df_raw = load_data()

# Filter for Master rows for general stats
df_master = df_raw[df_raw['type'] == 'Master'].copy()

# 3. Sidebar & Global Filtering System
st.sidebar.header("🎛 Dashboard Filters")

# Province Filter
provinces = sorted(df_master['province'].unique().tolist())
selected_province = st.sidebar.multiselect("Filter by Province", options=provinces, default=provinces)

# Issue Area Filter
issues = sorted(df_master['issue_area'].unique().tolist())
selected_issue = st.sidebar.multiselect("Filter by Issue Area", options=issues, default=issues)

# Status Filter
statuses = sorted(df_master['project_status'].dropna().unique().tolist())
selected_status = st.sidebar.multiselect("Filter by Project Status", options=statuses, default=statuses)

# Specific Project Search
project_list = ["All Projects"] + sorted(df_master['project_name_full'].unique().tolist())
selected_project = st.sidebar.selectbox("Deep-Dive into Specific Project", options=project_list)

# Apply Global Filters to df_master
filtered_df = df_master[
    (df_master['province'].isin(selected_province)) &
    (df_master['issue_area'].isin(selected_issue)) &
    (df_master['project_status'].isin(selected_status))
]

# 4. Main Dashboard Layout
st.title("📊 M&E Project Tracking Dashboard")
st.markdown("---")

# Section 1: Executive KPIs
st.subheader("📌 Executive Overview")
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.metric("Total Projects", f"{len(filtered_df)} โครงการ")

with kpi2:
    total_budget = filtered_df['budget_thb'].sum()
    st.metric("Total Budget Allocated", f"{total_budget:,.2f} THB")

with kpi3:
    completed_data = len(filtered_df[filtered_df['tracker_status'] == 'ส่งข้อมูลครบถ้วน'])
    st.metric("Data Completion Rate", f"{(completed_data/len(filtered_df)*100) if len(filtered_df)>0 else 0:.1f}%")

st.markdown("---")

# Section 2: Data Completeness & Action Needed Roster
st.subheader("⚠️ Action Needed Roster")
# Filter projects that need action
action_df = filtered_df[filtered_df['action_needed'].notna() & (filtered_df['action_needed'] != "")]

if not action_df.empty:
    display_action = action_df[['project_code', 'project_name_th', 'tracker_status', 'action_needed']]
    
    # Styling function
    def highlight_status(val):
        color = '#ffcccc' if "บางส่วน" in str(val) or "ไม่ครบ" in str(val) else 'transparent'
        return f'background-color: {color}'

    st.dataframe(
        display_action.style.applymap(highlight_status, subset=['tracker_status']),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("✅ No urgent actions needed for the filtered selection.")

st.markdown("---")

# Section 3: Overall Analysis Charts
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("💰 Budget by Issue Area")
    budget_chart = px.bar(
        filtered_df.groupby('issue_area')['budget_thb'].sum().reset_index(),
        y='issue_area',
        x='budget_thb',
        orientation='h',
        color='issue_area',
        labels={'budget_thb': 'Total Budget (THB)', 'issue_area': 'Area'},
        template="plotly_white"
    )
    st.plotly_chart(budget_chart, use_container_width=True)

with col_chart2:
    st.subheader("📝 Data Tracking Status")
    status_chart = px.pie(
        filtered_df,
        names='tracker_status',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
        template="plotly_white"
    )
    st.plotly_chart(status_chart, use_container_width=True)

# Section 4: Project Deep-Dive View
if selected_project != "All Projects":
    st.markdown("---")
    st.subheader(f"🔍 Deep-Dive: {selected_project}")
    
    # Get the data for the specific project from the master list
    project_data = df_master[df_master['project_name_full'] == selected_project].iloc[0]
    
    # Create an info layout
    d1, d2 = st.columns(2)
    with d1:
        st.info(f"**Raw Outcome:**\n\n{project_data['raw_outcome']}")
        st.warning(f"**Signals:**\n\n{project_data['signal'] if pd.notna(project_data['signal']) else 'No signals recorded'}")
        
    with d2:
        st.success(f"**Quotations/Comments:**\n\n{project_data['quotation'] if pd.notna(project_data['quotation']) else 'No quotations available'}")
        st.markdown(f"**💡 Recommendations:**\n\n{project_data['recommendation'] if pd.notna(project_data['recommendation']) else 'None'}")

    # Show additional rows related to this project (Quantitative/Qualitative)
    st.write("**Related Data Entries (Raw Log):**")
    related_rows = df_raw[df_raw['project_code'] == project_data['project_code']]
    st.dataframe(related_rows[['type', 'mentomentor_interviewer', 'last_data_date', 'raw_outcome', 'recommendation']], use_container_width=True)

# Footer
st.markdown("---")
st.caption("Data Scientist M&E Dashboard | Streamlit & Plotly | รองรับภาษาไทย (UTF-8-SIG)")