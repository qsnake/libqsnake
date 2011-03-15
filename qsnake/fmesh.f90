module fmesh

implicit none

integer, parameter:: dp=kind(0.d0)

contains

subroutine mesh_log(r_min, r_max, a, N, mesh)
real(dp), intent(in) :: r_min
real(dp), intent(in) :: r_max
real(dp), intent(in) :: a
integer, intent(in) :: N
real(dp), intent(out) :: mesh(N+1)

integer :: i
real(dp) :: C
if (N > 1) then
    C = (r_max - r_min) / (a**(N/(N-1.0_dp)) - 1)
    do i = 0, N
        mesh(i+1) = (exp(i*log(a)/(N-1.0_dp)) - 1) * C + r_min
    enddo
else if (N == 1) then
    mesh(1) = r_min
    mesh(2) = r_max
else
    stop "mesh_log() requires N >= 1"
endif
end subroutine

subroutine mesh_exp(r_min, r_max, a, N, mesh)
real(dp), intent(in) :: r_min
real(dp), intent(in) :: r_max
real(dp), intent(in) :: a
integer, intent(in) :: N
real(dp), intent(out) :: mesh(N+1)

integer :: i
if (N < 1) stop "mesh_exp() requires N >= 1"
do i = 0, N
    mesh(i+1) = (exp(i*log(a)/N) - 1) / (a - 1)  * (r_max - r_min) + r_min
enddo
end subroutine

subroutine mesh_hyp(r_min, r_max, a, N, mesh)
real(dp), intent(in) :: r_min
real(dp), intent(in) :: r_max
real(dp), intent(in) :: a
integer, intent(in) :: N
real(dp), intent(out) :: mesh(N+1)

integer :: i
if (N < 1) stop "mesh_exp() requires N >= 1"
do i = 0, N
    mesh(i+1) = i * (a - 1) / (a*N - i)  * (r_max - r_min) + r_min
enddo
end subroutine

end module
