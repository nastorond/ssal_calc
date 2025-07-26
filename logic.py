# logic.py

# calculate_profits 함수는 기존 코드와 동일하게 유지합니다.
def calculate_profits(inputs):
    """입력값을 받아 각 비약의 수익을 계산하고 결과를 반환합니다."""
    try:
        oil = float(inputs["oil"].replace(",", "") or 0)
        item = float(inputs["item"].replace(",", "") or 0)
        stone = float(inputs["stone"].replace(",", "") or 0)
        celebration_price = float(inputs["celebration"].replace(",", "") or 0)
        recharge_price = float(inputs["recharge"].replace(",", "") or 0)
        small_recharge_price = float(inputs["small_recharge"].replace(",", "") or 0)
        base_cost = oil * 10 + item * 5 + stone * 2 + 1000
        base_cost2 = oil * 10 + item * 3 + stone * 1 + 1000
        base_cost3 = oil * 5 + item * 2 + stone * 1 + 1000
        profit_celebration = (celebration_price * 3 - base_cost) * 100 * 0.95 if celebration_price > 0 else 0
        profit_recharge = (recharge_price * 3 - base_cost2) * 100 * 0.95 if recharge_price > 0 else 0
        profit_small_recharge = (small_recharge_price * 6 - base_cost3) * 100 * 0.95 if small_recharge_price > 0 else 0
        result_text = (
            f"경축비 {profit_celebration:,.0f} 원\n"
            f"재획비 {profit_recharge:,.0f} 원\n"
            f"소형 재획비 {profit_small_recharge:,.0f} 원"
        )
        return result_text, "black"
    except (ValueError, TypeError):
        return "모든 칸에 숫자를 올바르게 입력해주세요.", "#FF4136"
    except Exception as e:
        return f"알 수 없는 오류가 발생했습니다:\n{e}", "#FF4136"

# --------------------------------------------------------------------
# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ 이 함수를 수정했습니다. ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# --------------------------------------------------------------------
def calculate_fatigue_profit(seed_price, oil_price, fatigue_count):
    """
    피로도 소모 시 쥬니퍼베리 씨앗 오일 제작/판매 이윤을 계산합니다.
    fatigue_count가 비어있으면 500으로 계산합니다.
    """
    try:
        # 입력 값 검증 및 숫자 변환
        seed_price = float(seed_price.replace(",", "") or 0)
        oil_price = float(oil_price.replace(",", "") or 0)

        # [수정] fatigue_count가 비어있으면 500을, 아니면 해당 값을 사용
        fatigue_limit = float(fatigue_count or 500)

        # 고정값 설정
        fatigue_per_craft = 1
        seeds_per_craft = 6
        cost_per_craft = 1000
        success_rate = 0.9
        auction_fee = 0.95

        # 총 제작 시도 횟수
        num_attempts = fatigue_limit // fatigue_per_craft
        
        # 1회 제작 시도 비용
        cost_per_attempt = (seed_price * seeds_per_craft) + cost_per_craft

        # 총 제작 비용
        total_cost = num_attempts * cost_per_attempt

        # 예상 성공 수량
        expected_successes = num_attempts * success_rate

        # 총 예상 수익 (수수료 적용)
        total_revenue = (expected_successes * oil_price) * auction_fee

        # 최종 이윤
        final_profit = total_revenue - total_cost
        
        # [수정] 결과 텍스트에 실제 계산에 사용된 피로도 값을 표시
        return (
            f"피로도 {int(fatigue_limit)} 소모 시 예상 이윤:\n"
            f"{final_profit:,.0f} 메소"
        )
    except (ValueError, TypeError):
        return "가격을 숫자로 올바르게 입력해주세요."
    except Exception as e:
        return f"계산 중 오류가 발생했습니다:\n{e}"